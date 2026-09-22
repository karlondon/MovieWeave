#!/bin/bash
# MovieWeave v4.0 - Production Push (Docker)

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   MovieWeave v4.0 - Production Deployment                  ║"
echo "╚════════════════════════════════════════════════════════════╝"

cd /tmp/MovieWeave

echo "Building Docker image..."
docker build -t movieweave:4.0 . --quiet

echo "Starting services with docker-compose..."
docker-compose down 2>/dev/null || true
docker-compose up -d

sleep 3

echo "Verifying services..."
docker-compose ps

echo ""
echo "✅ MovieWeave v4.0 is LIVE!"
echo ""
echo "Access at:"
echo "  Dashboard: http://localhost:5000"
echo "  API: http://localhost:5000/api/health"
echo ""
echo "Commands:"
echo "  Logs: docker-compose logs -f web"
echo "  Stop: docker-compose down"
echo "  Restart: docker-compose restart"
