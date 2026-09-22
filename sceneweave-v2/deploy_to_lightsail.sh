#!/bin/bash
# ==============================================================================
# deploy_to_lightsail.sh - Deploy SceneWeave MVP to AWS Lightsail Production
# ==============================================================================

set -e

# Configuration
LIGHTSAIL_IP="34.229.168.102"
LIGHTSAIL_USER="ubuntu"
PEM_KEY_PATH="/Users/karthiksankaran/MovieWeave/pem-key/NarrativeFilm-instance.pem"
PROJECT_LOCAL_PATH="/Users/karthiksankaran/MovieWeave/sceneweave-v2"
PROJECT_REMOTE_PATH="/home/ubuntu/sceneweave-v2"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  ${1}${NC}"; }
log_success() { echo -e "${GREEN}✅ ${1}${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  ${1}${NC}"; }
log_error() { echo -e "${RED}❌ ${1}${NC}"; }

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo "🚀 SceneWeave MVP - Lightsail Deployment Script"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# STEP 1: Verify Prerequisites
log_info "STEP 1: Verifying prerequisites..."

if [ ! -f "$PEM_KEY_PATH" ]; then
    log_error "PEM key not found at: $PEM_KEY_PATH"
    exit 1
fi
log_success "PEM key found"

if [ ! -d "$PROJECT_LOCAL_PATH" ]; then
    log_error "Local project not found at: $PROJECT_LOCAL_PATH"
    exit 1
fi
log_success "Local project found"

log_info "Testing SSH connection to Lightsail..."
if ssh -i "$PEM_KEY_PATH" -o ConnectTimeout=5 "$LIGHTSAIL_USER@$LIGHTSAIL_IP" "echo 'SSH OK'" > /dev/null 2>&1; then
    log_success "SSH connection successful"
else
    log_error "Cannot connect to $LIGHTSAIL_IP via SSH"
    exit 1
fi

echo ""

# STEP 2: Prepare Remote Directories
log_info "STEP 2: Creating remote directories..."

ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" bash << 'EOF'
mkdir -p /home/ubuntu/sceneweave-v2
mkdir -p /data/sceneweave/{uploads,output,temp,logs,assets}
chmod 755 /data/sceneweave/*
echo "✅ Remote directories created"
EOF

log_success "Remote directories ready"
echo ""

# STEP 3: Transfer Project Files
log_info "STEP 3: Transferring project files to Lightsail..."

rsync -avz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.pytest_cache' \
    --exclude='.env' \
    --exclude='logs' \
    --exclude='*.log' \
    --exclude='.DS_Store' \
    -e "ssh -i $PEM_KEY_PATH" \
    "$PROJECT_LOCAL_PATH/" \
    "$LIGHTSAIL_USER@$LIGHTSAIL_IP:$PROJECT_REMOTE_PATH/"

log_success "Project files transferred"

# STEP 4: Setup Python Environment
log_info "STEP 4: Setting up Python environment on Lightsail..."

ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" bash << 'EOF'
cd /home/ubuntu/sceneweave-v2/backend
python3 --version
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Python environment ready"
EOF

log_success "Python environment configured"
echo ""

# STEP 5: Deploy Production Configuration
log_info "STEP 5: Deploying production configuration..."

ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" bash << 'EOF'
cd /home/ubuntu/sceneweave-v2
cp .env.production .env 2>/dev/null || cp .env.example .env
cp .env backend/.env
EOF

log_success "Production configuration deployed"
echo ""

# STEP 6: Create Systemd Service
log_info "STEP 6: Creating systemd service..."

ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" sudo tee /etc/systemd/system/sceneweave.service > /dev/null << 'EOFSERVICE'
[Unit]
Description=SceneWeave MVP API Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/sceneweave-v2/backend
Environment="PATH=/home/ubuntu/sceneweave-v2/backend/venv/bin"
ExecStart=/home/ubuntu/sceneweave-v2/backend/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=10
StandardOutput=append:/data/sceneweave/logs/sceneweave.log
StandardError=append:/data/sceneweave/logs/sceneweave.error.log

[Install]
WantedBy=multi-user.target
EOFSERVICE

ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" bash << 'EOF'
sudo systemctl daemon-reload
sudo systemctl enable sceneweave.service
echo "✅ Systemd service created"
EOF

log_success "Systemd service configured"
echo ""

# STEP 7: Start Service
log_info "STEP 7: Starting SceneWeave service..."

ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" bash << 'EOF'
sudo systemctl restart sceneweave.service
sleep 3
if sudo systemctl is-active --quiet sceneweave.service; then
    echo "✅ Service running"
else
    echo "❌ Service failed"
    sudo systemctl status sceneweave.service
    exit 1
fi
EOF

log_success "SceneWeave service started"
echo ""

# STEP 8: Verify
log_info "STEP 8: Verifying deployment..."
sleep 2
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://$LIGHTSAIL_IP:8000/api/health)

if [ "$HEALTH" = "200" ]; then
    log_success "API is healthy!"
else
    log_warning "Health check returned HTTP $HEALTH"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
log_success "🎉 DEPLOYMENT COMPLETE!"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}📍 Production Server:${NC}"
echo "   IP:           http://$LIGHTSAIL_IP:8000"
echo "   API Docs:     http://$LIGHTSAIL_IP:8000/docs"
echo "   Domain:       movieweave.myblognow.uk"
echo ""
echo -e "${BLUE}📚 Useful Commands:${NC}"
echo "   Logs:    ssh -i $PEM_KEY_PATH ubuntu@$LIGHTSAIL_IP tail -f /data/sceneweave/logs/sceneweave.log"
echo "   Status:  ssh -i $PEM_KEY_PATH ubuntu@$LIGHTSAIL_IP sudo systemctl status sceneweave"
echo "   Restart: ssh -i $PEM_KEY_PATH ubuntu@$LIGHTSAIL_IP sudo systemctl restart sceneweave"
echo ""
echo "════════════════════════════════════════════════════════════════════════════════"

echo ""
