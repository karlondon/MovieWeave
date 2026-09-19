#!/bin/bash

# MovieWeave Initial Setup Script - Part 1
# Run this on the Lightsail instance: bash scripts/initial-setup.sh

set -e

echo "🎬 MovieWeave - Initial Setup Script"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⚠️  Run with sudo: sudo bash scripts/initial-setup.sh${NC}"
    exit 1
fi

# Update system packages
echo -e "${BLUE}📦 Updating system packages...${NC}"
apt-get update
apt-get upgrade -y

# Install Docker
echo -e "${BLUE}🐳 Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker ubuntu
    rm get-docker.sh
    echo -e "${GREEN}✅ Docker installed${NC}"
else
    echo -e "${GREEN}✅ Docker already installed${NC}"
fi

# Install Docker Compose
echo -e "${BLUE}📝 Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
else
    echo -e "${GREEN}✅ Docker Compose already installed${NC}"
fi

# Install Python and dependencies
echo -e "${BLUE}🐍 Installing Python 3.11...${NC}"
apt-get install -y python3.11 python3.11-venv python3-pip
python3.11 --version

# Install FFmpeg
echo -e "${BLUE}🎥 Installing FFmpeg...${NC}"
apt-get install -y ffmpeg

# Install Nginx
echo -e "${BLUE}🌐 Installing Nginx...${NC}"
apt-get install -y nginx
systemctl enable nginx

# Install Git
echo -e "${BLUE}📂 Installing Git...${NC}"
apt-get install -y git

# Install AWS CLI
echo -e "${BLUE}☁️  Installing AWS CLI...${NC}"
apt-get install -y awscli

# Install Node.js
echo -e "${BLUE}📦 Installing Node.js...${NC}"
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Create application directories
echo -e "${BLUE}📁 Creating application directories...${NC}"
mkdir -p /opt/movieweave/{data,logs,config}
mkdir -p /opt/movieweave/data/{uploads,output,temp}
chown -R ubuntu:ubuntu /opt/movieweave
chmod -R 755 /opt/movieweave

# Configure firewall
echo -e "${BLUE}🔒 Configuring firewall...${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp
ufw allow 10588/tcp
ufw --force enable

# Create swap file
echo -e "${BLUE}💾 Creating swap file...${NC}"
if [ ! -f /swapfile ]; then
    fallocate -l 4G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
    echo -e "${GREEN}✅ Swap file created (4GB)${NC}"
fi

echo -e "${GREEN}✅ Part 1 Complete!${NC}"
