#!/bin/bash

# MovieWeave Deployment Script
# Run this after initial setup: bash scripts/deploy.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🎬 MovieWeave - Deployment Script${NC}"
echo "=================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "Run: cp .env.example .env"
    echo "Then edit .env with your AWS credentials"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not installed! Run initial-setup.sh first${NC}"
    exit 1
fi

echo -e "${BLUE}🔧 Pre-deployment checks...${NC}"

# Create required directories
mkdir -p data/{uploads,output,temp}
mkdir -p logs

# Load environment variables
set -a
source .env
set +a

echo -e "${GREEN}✅ Environment loaded${NC}"

# Build Docker images
echo -e "${BLUE}🐳 Building Docker images...${NC}"
docker-compose build

echo -e "${GREEN}✅ Docker images built${NC}"

# Start services
echo -e "${BLUE}🚀 Starting services...${NC}"
docker-compose up -d

sleep 5

# Check if services are running
echo -e "${BLUE}📊 Checking service status...${NC}"
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Services running${NC}"
else
    echo -e "${RED}❌ Services failed to start${NC}"
    docker-compose logs
    exit 1
fi

# Display summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ MovieWeave Deployed Successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "🌐 Access the application:"
echo "   Local: http://localhost:8000"
echo "   Public: https://movieweave.myblognow.uk (after DNS setup)"
echo ""
echo "📊 Service Status:"
docker-compose ps
echo ""
echo "📋 API Documentation:"
echo "   http://34.204.47.202:8000/docs"
echo ""
echo "🔍 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
echo "✅ Next: Configure domain and SSL certificate"
echo ""
