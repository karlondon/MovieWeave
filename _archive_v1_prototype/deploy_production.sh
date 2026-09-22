#!/bin/bash
# MovieWeave Production Deployment - Part 1: Setup & Dependencies

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   MovieWeave Production Deployment v3.0                    ║"
echo "╚════════════════════════════════════════════════════════════╝"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

DOMAIN="${1:-movieweave.local}"
PORT="${2:-5000}"
WORKERS="${3:-4}"
APP_DIR="/opt/movieweave"
VENV_DIR="$APP_DIR/venv"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Domain: $DOMAIN"
echo "  Port: $PORT"
echo "  Workers: $WORKERS"
echo "  App Dir: $APP_DIR"

# Step 1: System Dependencies
echo -e "\n${YELLOW}Step 1: Installing system dependencies...${NC}"
sudo apt-get update
sudo apt-get install -y python3.9 python3-pip python3-venv ffmpeg nginx supervisor redis-server

# Step 2: Create app directory
echo -e "\n${YELLOW}Step 2: Setting up application directory...${NC}"
sudo mkdir -p $APP_DIR
cd $APP_DIR

# Step 3: Create Python virtual environment
echo -e "\n${YELLOW}Step 3: Creating Python virtual environment...${NC}"
sudo python3.9 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Step 4: Install Python dependencies
echo -e "\n${YELLOW}Step 4: Installing Python dependencies...${NC}"
sudo $VENV_DIR/bin/pip install --upgrade pip
sudo $VENV_DIR/bin/pip install flask pillow gunicorn redis

# Step 5: Create necessary directories
echo -e "\n${YELLOW}Step 5: Creating necessary directories...${NC}"
sudo mkdir -p $APP_DIR/output/videos
sudo mkdir -p $APP_DIR/output/scenes
sudo mkdir -p $APP_DIR/uploads
sudo mkdir -p $APP_DIR/logs
sudo chown -R www-data:www-data $APP_DIR

echo -e "\n${GREEN}✓ System setup complete!${NC}"
