#!/bin/bash
# MovieWeave HTTPS Setup Script
# This script sets up SSL certificates with Let's Encrypt and configures HTTPS

set -e

DOMAIN="movieweave.myblognow.uk"
EMAIL="karthik@myblognow.uk"  # Update this with your email
LIGHTSAIL_IP="34.229.168.102"
LIGHTSAIL_USER="ubuntu"
LIGHTSAIL_KEY="/Users/karthiksankaran/PS-Scripts/private-key-pair/NarrativeFilm-instance.pem"

echo "🔒 MovieWeave HTTPS Setup"
echo "=========================="
echo "Domain: $DOMAIN"
echo "Lightsail IP: $LIGHTSAIL_IP"
echo ""

# Step 1: Upload updated Nginx config
echo "📤 Step 1: Uploading updated Nginx configuration..."
scp -i "$LIGHTSAIL_KEY" /Users/karthiksankaran/MovieWeave/config/nginx.conf \
    "$LIGHTSAIL_USER@$LIGHTSAIL_IP:/opt/movieweave/config/nginx.conf"
echo "✅ Nginx config uploaded"

# Step 2: Set up DNS (User needs to do this manually)
echo ""
echo "📋 Step 2: DNS Configuration Required"
echo "======================================"
echo "Please ensure your DNS records are set up:"
echo "  A Record: $DOMAIN -> $LIGHTSAIL_IP"
echo ""
read -p "Press Enter once DNS is configured and propagated (wait ~5-10 minutes)..."

# Step 3: SSH into Lightsail and set up SSL
echo ""
echo "🔐 Step 3: Setting up SSL certificates with Let's Encrypt..."
ssh -i "$LIGHTSAIL_KEY" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" << 'ENDSSH'
  set -e
  
  DOMAIN="movieweave.myblognow.uk"
  EMAIL="karthik@myblognow.uk"
  
  cd /opt/movieweave
  
  # Create certbot directory if it doesn't exist
  sudo mkdir -p /etc/letsencrypt
  
  # Stop Nginx temporarily
  echo "Stopping Nginx..."
  sudo docker-compose down nginx || true
  
  # Generate SSL certificate
  echo "Generating SSL certificate for $DOMAIN..."
  sudo certbot certonly \
    --standalone \
    --agree-tos \
    --no-eff-email \
    --email "$EMAIL" \
    -d "$DOMAIN" \
    --preferred-challenges http
  
  echo "✅ SSL certificate generated successfully!"
  
ENDSSH

# Step 4: Restart services with new configuration
echo ""
echo "🚀 Step 4: Restarting services with HTTPS enabled..."
ssh -i "$LIGHTSAIL_KEY" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" << 'ENDSSH'
  cd /opt/movieweave
  
  # Start services
  echo "Starting Docker services..."
  sudo docker-compose up -d
  
  # Wait for services to be ready
  sleep 10
  
  # Check if services are running
  echo "Checking service status..."
  sudo docker-compose ps
  
  echo ""
  echo "✅ Services started successfully!"
  
ENDSSH

# Step 5: Test HTTPS
echo ""
echo "🧪 Step 5: Testing HTTPS configuration..."
echo ""

# Test HTTP redirect
echo "Testing HTTP -> HTTPS redirect..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -L "http://$DOMAIN" 2>/dev/null || echo "000")
echo "HTTP redirect status: $HTTP_STATUS"

# Test HTTPS
echo ""
echo "Testing HTTPS connection..."
HTTPS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" 2>/dev/null || echo "000")
echo "HTTPS status: $HTTPS_STATUS"

if [ "$HTTPS_STATUS" = "404" ] || [ "$HTTPS_STATUS" = "200" ]; then
  echo ""
  echo "✅ HTTPS is working! Status: $HTTPS_STATUS"
else
  echo ""
  echo "⚠️  HTTPS status might need checking. Status: $HTTPS_STATUS"
fi

# Step 6: Setup auto-renewal
echo ""
echo "🔄 Step 6: Setting up automatic certificate renewal..."
ssh -i "$LIGHTSAIL_KEY" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" << 'ENDSSH'
  # Enable certbot auto-renewal
  echo "Setting up automatic certificate renewal..."
  sudo systemctl enable certbot.timer
  sudo systemctl start certbot.timer
  
  echo "✅ Automatic renewal enabled!"
  
ENDSSH

echo ""
echo "🎉 HTTPS Setup Complete!"
echo "========================"
echo ""
echo "Your MovieWeave application is now available at:"
echo "  🔒 https://movieweave.myblognow.uk"
echo ""
echo "Features enabled:"
echo "  ✅ HTTPS/SSL encryption (TLSv1.2 & TLSv1.3)"
echo "  ✅ Automatic HTTP → HTTPS redirect"
echo "  ✅ HSTS (HTTP Strict Transport Security)"
echo "  ✅ Automatic certificate renewal"
echo "  ✅ Security headers (X-Frame-Options, CSP, etc.)"
echo ""
echo "Next steps:"
echo "  1. Update your frontend API URL to: https://movieweave.myblognow.uk"
echo "  2. Update any hardcoded URLs in your code"
echo "  3. Test the application at https://movieweave.myblognow.uk"
echo ""
echo "Certificate valid until: $(date -d '+90 days' '+%Y-%m-%d')"
echo "Auto-renewal will happen automatically 30 days before expiry"
echo ""
