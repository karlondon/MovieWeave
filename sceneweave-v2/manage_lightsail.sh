#!/bin/bash
# ==============================================================================
# manage_lightsail.sh - Helper script to manage SceneWeave on Lightsail
# ==============================================================================

LIGHTSAIL_IP="34.229.168.102"
LIGHTSAIL_USER="ubuntu"
PEM_KEY_PATH="/Users/karthiksankaran/MovieWeave/pem-key/NarrativeFilm-instance.pem"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

usage() {
    echo "SceneWeave Lightsail Management Tool"
    echo ""
    echo "Usage: ./manage_lightsail.sh <command>"
    echo ""
    echo "Commands:"
    echo "  status      - Show service status"
    echo "  logs        - Tail service logs"
    echo "  restart     - Restart the service"
    echo "  stop        - Stop the service"
    echo "  start       - Start the service"
    echo "  health      - Check API health"
    echo "  ssh         - SSH into server"
    echo "  update      - Deploy latest code (no restart)"
    echo "  redeploy    - Full deployment with restart"
    echo ""
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

case "$1" in
    status)
        echo -e "${BLUE}📊 Service Status${NC}"
        ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" sudo systemctl status sceneweave.service
        ;;
    logs)
        echo -e "${BLUE}📝 Service Logs (follow)${NC}"
        ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" tail -f /data/sceneweave/logs/sceneweave.log
        ;;
    restart)
        echo -e "${BLUE}🔄 Restarting service...${NC}"
        ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" sudo systemctl restart sceneweave.service
        echo -e "${GREEN}✅ Service restarted${NC}"
        ;;
    stop)
        echo -e "${BLUE}🛑 Stopping service...${NC}"
        ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" sudo systemctl stop sceneweave.service
        echo -e "${GREEN}✅ Service stopped${NC}"
        ;;
    start)
        echo -e "${BLUE}▶️  Starting service...${NC}"
        ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP" sudo systemctl start sceneweave.service
        echo -e "${GREEN}✅ Service started${NC}"
        ;;
    health)
        echo -e "${BLUE}🏥 Checking API Health${NC}"
        RESPONSE=$(curl -s -w "\n%{http_code}" http://$LIGHTSAIL_IP:8000/api/health)
        HTTP_CODE=$(echo "$RESPONSE" | tail -1)
        BODY=$(echo "$RESPONSE" | head -1)
        
        if [ "$HTTP_CODE" = "200" ]; then
            echo -e "${GREEN}✅ API is healthy${NC}"
            echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
        else
            echo -e "${RED}❌ API returned HTTP $HTTP_CODE${NC}"
        fi
        ;;
    ssh)
        echo -e "${BLUE}🔌 SSH to Lightsail${NC}"
        ssh -i "$PEM_KEY_PATH" "$LIGHTSAIL_USER@$LIGHTSAIL_IP"
        ;;
    update)
        echo -e "${BLUE}📦 Updating code (no restart)${NC}"
        bash /Users/karthiksankaran/MovieWeave/sceneweave-v2/deploy_to_lightsail.sh update
        ;;
    redeploy)
        echo -e "${BLUE}🚀 Full redeploy with restart${NC}"
        bash /Users/karthiksankaran/MovieWeave/sceneweave-v2/deploy_to_lightsail.sh
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        usage
        exit 1
        ;;
esac
