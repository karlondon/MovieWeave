#!/bin/bash
# ==============================================================================
# test_production.sh - Test SceneWeave MVP on Lightsail Production Server
# ==============================================================================

LIGHTSAIL_IP="34.229.168.102"
API_URL="http://$LIGHTSAIL_IP:8000"
RESULTS_FILE="production_test_results.log"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo "🧪 SceneWeave MVP - Production Testing (Lightsail)"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Test 1: Health Check
echo -e "${YELLOW}[TEST 1]${NC} API Health Check"
RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/api/health")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ PASS${NC}: Server is healthy"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
else
    echo -e "${RED}❌ FAIL${NC}: HTTP $HTTP_CODE"
    exit 1
fi
echo ""

# Test 2: Upload File
echo -e "${YELLOW}[TEST 2]${NC} File Upload to Production"
TEST_FILE="test_story_prod.txt"
cat > "$TEST_FILE" << 'EOF'
The sun rose over the misty mountains.
A lone traveler journeyed through the ancient forest.
Strange sounds echoed through the trees.
EOF

UPLOAD_RESPONSE=$(curl -s -X POST -F "file=@$TEST_FILE" "$API_URL/api/upload")
JOB_ID=$(echo "$UPLOAD_RESPONSE" | grep -o '"job_id":"[^"]*' | cut -d'"' -f4)

if [ ! -z "$JOB_ID" ]; then
    echo -e "${GREEN}✅ PASS${NC}: File uploaded"
    echo "   Job ID: $JOB_ID"
else
    echo -e "${RED}❌ FAIL${NC}: Upload failed"
    echo "$UPLOAD_RESPONSE"
    exit 1
fi
echo ""

# Test 3: Check Job Status
echo -e "${YELLOW}[TEST 3]${NC} Job Status"
STATUS_RESPONSE=$(curl -s "$API_URL/api/status/$JOB_ID")

if echo "$STATUS_RESPONSE" | grep -q "pending\|processing"; then
    echo -e "${GREEN}✅ PASS${NC}: Job status retrieved"
    echo "$STATUS_RESPONSE" | jq '.' 2>/dev/null || echo "$STATUS_RESPONSE"
else
    echo -e "${RED}❌ FAIL${NC}: Status check failed"
    exit 1
fi
echo ""

# Test 4: List All Jobs
echo -e "${YELLOW}[TEST 4]${NC} List All Jobs"
JOBS_RESPONSE=$(curl -s "$API_URL/api/jobs")

if echo "$JOBS_RESPONSE" | grep -q "job_id"; then
    JOB_COUNT=$(echo "$JOBS_RESPONSE" | grep -o '"job_id"' | wc -l)
    echo -e "${GREEN}✅ PASS${NC}: Retrieved $JOB_COUNT jobs"
else
    echo -e "${RED}❌ FAIL${NC}: Jobs list failed"
fi
echo ""

# Cleanup
rm -f "$TEST_FILE"

echo "════════════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ All Production Tests Passed!${NC}"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}📍 Production Details:${NC}"
echo "   API: $API_URL"
echo "   Docs: $API_URL/docs"
echo ""
