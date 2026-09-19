#!/bin/bash

# MovieWeave Health Check Script
# Run this to verify all services are running properly

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🎬 MovieWeave Health Check${NC}"
echo "=============================="
echo ""

# Check Docker
echo -e "${BLUE}Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker installed${NC}"
    docker --version
else
    echo -e "${RED}❌ Docker not installed${NC}"
fi

# Check Docker Compose
echo -e "${BLUE}Checking Docker Compose...${NC}"
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
    docker-compose --version
else
    echo -e "${RED}❌ Docker Compose not installed${NC}"
fi

# Check if services are running
echo ""
echo -e "${BLUE}Service Status:${NC}"
docker-compose ps

# Health check endpoint
echo ""
echo -e "${BLUE}API Health Check:${NC}"
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ FastAPI is running${NC}"
    curl -s http://localhost:8000/health | jq '.'
else
    echo -e "${RED}❌ FastAPI is not responding${NC}"
fi

# Check S3 connection
echo ""
echo -e "${BLUE}AWS S3 Connection:${NC}"
if aws s3 ls movieweave-storage 2>/dev/null; then
    echo -e "${GREEN}✅ S3 bucket is accessible${NC}"
else
    echo -e "${RED}❌ S3 bucket not accessible (check credentials)${NC}"
fi

# Disk usage
echo ""
echo -e "${BLUE}Disk Usage:${NC}"
echo -e "System:"
df -h / | tail -1
echo -e "\nApplication:"
du -sh /opt/movieweave/ 2>/dev/null || echo "Not applicable"
du -sh ./data/ 2>/dev/null || echo "Not applicable"

# Memory usage
echo ""
echo -e "${BLUE}Memory Usage:${NC}"
free -h

# Port availability
echo ""
echo -e "${BLUE}Port Status:${NC}"
for port in 80 443 8000 10588; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${GREEN}✅ Port $port is open${NC}"
    else
        echo -e "${YELLOW}⚠️  Port $port is closed${NC}"
    fi
done

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Health check complete!${NC}"
echo -e "${GREEN}========================================${NC}"
