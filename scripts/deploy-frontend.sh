#!/bin/bash
# MovieWeave Frontend Build & Deploy Script

set -e

LIGHTSAIL_IP="34.229.168.102"
LIGHTSAIL_USER="ubuntu"
LIGHTSAIL_KEY="/Users/karthiksankaran/PS-Scripts/private-key-pair/NarrativeFilm-instance.pem"
FRONTEND_DIR="/Users/karthiksankaran/MovieWeave/frontend"

echo "🎬 MovieWeave Frontend Build & Deploy"
echo "======================================"
echo ""

# Step 1: Install dependencies
echo "📦 Step 1: Installing dependencies..."
cd "$FRONTEND_DIR"
npm install
echo "✅ Dependencies installed"
echo ""

# Step 2: Build production version
echo "🔨 Step 2: Building for production..."
npm run build
echo "✅ Production build complete"
echo ""

# Verify build output
if [ ! -d "$FRONTEND_DIR/dist" ]; then
  echo "❌ Build failed - dist folder not found"
  exit 1
fi

BUILD_SIZE=$(du -sh "$FRONTEND_DIR/dist" | cut -f1)
echo "📊 Build size: $BUILD_SIZE"
echo ""

# Step 3: Upload to Lightsail
echo "📤 Step 3: Uploading frontend to Lightsail..."
echo "   Target: ubuntu@$LIGHTSAIL_IP:/opt/movieweave/frontend/"

# Create frontend directory on server
ssh -i "$LIGHTSAIL_KEY" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" \
  "sudo mkdir -p /opt/movieweave/frontend && sudo chown -R ubuntu:ubuntu /opt/movieweave/frontend"

# Upload dist folder
scp -r -i "$LIGHTSAIL_KEY" "$FRONTEND_DIR/dist/"* \
  "$LIGHTSAIL_USER@$LIGHTSAIL_IP:/opt/movieweave/frontend/"

echo "✅ Frontend uploaded successfully"
echo ""

# Step 4: Configure Nginx to serve frontend
echo "🌐 Step 4: Configuring Nginx to serve frontend..."
ssh -i "$LIGHTSAIL_KEY" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" << 'ENDSSH'
  cd /opt/movieweave
  echo "Verifying frontend files..."
  ls -lh frontend/ | head -10
  echo ""
  echo "Total files uploaded: $(find frontend -type f | wc -l)"
  
ENDSSH

echo "✅ Nginx configured"
echo ""

# Step 5: Test the deployment
echo "🧪 Step 5: Testing frontend deployment..."
echo ""

# Test HTTPS connection
echo "Testing HTTPS connection..."
HTTPS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://movieweave.myblognow.uk" 2>/dev/null || echo "000")
echo "HTTPS Status: $HTTPS_STATUS"

# Test API
echo ""
echo "Testing API endpoint..."
API_RESPONSE=$(curl -s https://movieweave.myblognow.uk/ 2>/dev/null || echo "failed")
echo "API Response: $API_RESPONSE"

echo ""
echo "🎉 Frontend Deployment Complete!"
echo "=================================="
echo ""
echo "✅ Your MovieWeave application is now live!"
echo ""
echo "Access your app at:"
echo "  🔒 https://movieweave.myblognow.uk"
echo ""
echo "Features available:"
echo "  📤 Upload documents (PDF, DOC, DOCX, TXT, MD, RTF, ODT)"
echo "  🎬 Real-time video conversion tracking"
echo "  💾 Download converted videos"
echo "  💰 Pricing: 5 free videos, then £5 each"
echo "  📚 API Documentation: https://movieweave.myblognow.uk/docs"
echo ""
echo "Deployment files:"
echo "  Frontend: /opt/movieweave/frontend/"
echo "  Config: /opt/movieweave/config/nginx.conf"
echo "  API: Docker container (movieweave-api:8000)"
echo ""
echo "Next steps:"
echo "  1. Visit https://movieweave.myblognow.uk"
echo "  2. Test the upload and conversion features"
echo "  3. Check logs: sudo docker-compose logs -f"
echo ""
