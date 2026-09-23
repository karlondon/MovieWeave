#!/bin/bash
# deploy_to_lightsail_direct.sh - Deploy SceneWeave to Lightsail server

set -e

# Configuration
LIGHTSAIL_IP="34.229.168.102"
SSH_KEY="/Users/karthiksankaran/MovieWeave/pem-key/NarrativeFilm-instance.pem"
SSH_USER="ubuntu"
REMOTE_PATH="/home/ubuntu/sceneweave"
DATA_PATH="/data/sceneweave"

echo "🚀 SceneWeave Deployment to Lightsail"
echo "======================================"
echo "IP: $LIGHTSAIL_IP"
echo "User: $SSH_USER"
echo "Remote Path: $REMOTE_PATH"
echo ""

# Check SSH key exists
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found: $SSH_KEY"
    exit 1
fi

# Set proper permissions on SSH key
chmod 600 "$SSH_KEY"

# Test SSH connection
echo "🔌 Testing SSH connection..."
if ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$SSH_USER@$LIGHTSAIL_IP" "echo '✅ SSH OK'" 2>/dev/null; then
    echo "✅ SSH connection successful"
else
    echo "❌ Cannot connect to $LIGHTSAIL_IP"
    echo "   Check if IP is correct and server is running"
    exit 1
fi

echo ""
echo "📤 Creating remote directories..."
ssh -i "$SSH_KEY" "$SSH_USER@$LIGHTSAIL_IP" << 'EOF'
sudo mkdir -p /home/ubuntu/sceneweave
sudo mkdir -p /data/sceneweave/{uploads,output,temp,logs}
sudo chown -R ubuntu:ubuntu /home/ubuntu/sceneweave
sudo chown -R ubuntu:ubuntu /data/sceneweave
echo "✅ Directories created"
EOF

echo ""
echo "📤 Uploading code to server (this may take a minute)..."
rsync -avz -e "ssh -i $SSH_KEY" \
    --exclude='node_modules' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    --exclude='.venv' \
    --exclude='venv' \
    /Users/karthiksankaran/MovieWeave/sceneweave-v2/ \
    "$SSH_USER@$LIGHTSAIL_IP:$REMOTE_PATH/"

echo "✅ Code uploaded"

echo ""
echo "🔧 Setting up Python environment on server..."
ssh -i "$SSH_KEY" "$SSH_USER@$LIGHTSAIL_IP" << 'EOF'
set -e

cd /home/ubuntu/sceneweave

# Update system
sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-pip python3-venv git

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate venv and install dependencies
source venv/bin/activate

pip install -q --upgrade pip
pip install -q -r backend/requirements.txt

echo "✅ Python dependencies installed"
EOF

echo ""
echo "🎬 Installing FFmpeg (for video composition)..."
ssh -i "$SSH_KEY" "$SSH_USER@$LIGHTSAIL_IP" << 'EOF'
sudo apt-get install -y -qq ffmpeg
ffmpeg -version | head -1
echo "✅ FFmpeg installed"
EOF

echo ""
echo "🤖 Installing Ollama & Kokoro TTS..."
ssh -i "$SSH_KEY" "$SSH_USER@$LIGHTSAIL_IP" << 'EOF'
# Check if Ollama is already installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "✅ Ollama already installed"
fi

# Start Ollama in background
ollama serve &
sleep 5

# Pull the Qwen model
ollama pull qwen:2.5-instruct-q4_K_M || echo "⚠️ Model already cached"

echo "✅ Ollama & Qwen ready"
EOF

echo ""
echo "⚙️ Creating systemd service..."
ssh -i "$SSH_KEY" "$SSH_USER@$LIGHTSAIL_IP" << 'EOF'
sudo tee /etc/systemd/system/sceneweave.service > /dev/null <<'SYSTEMD'
[Unit]
Description=SceneWeave Video Generation API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/sceneweave
Environment="PATH=/home/ubuntu/sceneweave/venv/bin"
ExecStart=/home/ubuntu/sceneweave/venv/bin/python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMD

sudo systemctl daemon-reload
sudo systemctl enable sceneweave
echo "✅ Systemd service created"
EOF

echo ""
echo "🚀 Starting SceneWeave API service..."
ssh -i "$SSH_KEY" "$SSH_USER@$LIGHTSAIL_IP" << 'EOF'
sudo systemctl start sceneweave
sleep 3
sudo systemctl status sceneweave --no-pager | head -5
echo "✅ Service started"
EOF

echo ""
echo "🏥 Verifying API is running..."
for i in {1..30}; do
    if curl -s "http://$LIGHTSAIL_IP:8000/api/health" | grep -q "healthy"; then
        echo "✅ API is healthy and responding"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "⚠️ API not responding yet, may still be starting"
    fi
    sleep 1
done

echo ""
echo "======================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "======================================"
echo ""
echo "📊 Your SceneWeave API is live at:"
echo ""
echo "  🌐 API:    http://$LIGHTSAIL_IP:8000"
echo "  📖 Docs:   http://$LIGHTSAIL_IP:8000/docs"
echo "  🎬 Video: http://$LIGHTSAIL_IP:8000/api/download/{job_id}"
echo ""
echo "🧪 Test it:"
echo "  curl http://$LIGHTSAIL_IP:8000/api/health"
echo ""
echo "📋 View logs:"
echo "  ssh -i $SSH_KEY $SSH_USER@$LIGHTSAIL_IP sudo journalctl -u sceneweave -f"
echo ""
echo "🚀 Ready to generate videos!"
echo ""
