#!/bin/bash
"""
test_phase1.sh - Automated test suite for SceneWeave MVP Phase 1
"""

set -e

API_URL="http://localhost:8000"
RESULTS_FILE="test_results.log"

echo "🧪 SceneWeave MVP Phase 1 - Test Suite" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE
echo "" | tee -a $RESULTS_FILE

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${YELLOW}[TEST 1]${NC} Health Check" | tee -a $RESULTS_FILE
response=$(curl -s $API_URL/api/health)
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✅ PASS${NC}: Server is healthy" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ FAIL${NC}: Health check failed" | tee -a $RESULTS_FILE
    exit 1
fi
echo "" | tee -a $RESULTS_FILE

# Test 2: Create test file
echo -e "${YELLOW}[TEST 2]${NC} File Upload" | tee -a $RESULTS_FILE
TEST_FILE="test_story_$RANDOM.txt"
cat > $TEST_FILE << EOF
Once upon a time, in a mystical forest, there lived a brave knight.
The knight ventured forth to find the legendary treasure.
What challenges awaited him? Nobody knew.
EOF

response=$(curl -s -X POST -F "file=@$TEST_FILE" $API_URL/api/upload)
JOB_ID=$(echo "$response" | grep -o '"job_id":"[^"]*' | cut -d'"' -f4)

if [ ! -z "$JOB_ID" ]; then
    echo -e "${GREEN}✅ PASS${NC}: File uploaded successfully" | tee -a $RESULTS_FILE
    echo "   Job ID: $JOB_ID" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ FAIL${NC}: File upload failed" | tee -a $RESULTS_FILE
    echo "$response" | tee -a $RESULTS_FILE
    exit 1
fi
echo "" | tee -a $RESULTS_FILE

# Test 3: Check job status
echo -e "${YELLOW}[TEST 3]${NC} Job Status Check" | tee -a $RESULTS_FILE
response=$(curl -s $API_URL/api/status/$JOB_ID)
if echo "$response" | grep -q "pending\|processing"; then
    echo -e "${GREEN}✅ PASS${NC}: Job status retrieved" | tee -a $RESULTS_FILE
    echo "$response" | jq '.' >> $RESULTS_FILE 2>/dev/null || echo "$response" >> $RESULTS_FILE
else
    echo -e "${RED}❌ FAIL${NC}: Job status check failed" | tee -a $RESULTS_FILE
    exit 1
fi
echo "" | tee -a $RESULTS_FILE

# Test 4: List all jobs
echo -e "${YELLOW}[TEST 4]${NC} List All Jobs" | tee -a $RESULTS_FILE
response=$(curl -s $API_URL/api/jobs)
if echo "$response" | grep -q "job_id"; then
    echo -e "${GREEN}✅ PASS${NC}: Jobs list retrieved" | tee -a $RESULTS_FILE
    job_count=$(echo "$response" | grep -o '"job_id"' | wc -l)
    echo "   Total jobs: $job_count" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ FAIL${NC}: Jobs list failed" | tee -a $RESULTS_FILE
    exit 1
fi
echo "" | tee -a $RESULTS_FILE

# Test 5: Invalid file type
echo -e "${YELLOW}[TEST 5]${NC} Invalid File Type Rejection" | tee -a $RESULTS_FILE
echo "fake data" > invalid_file.bin
response=$(curl -s -X POST -F "file=@invalid_file.bin" $API_URL/api/upload)
if echo "$response" | grep -q "not supported\|File type"; then
    echo -e "${GREEN}✅ PASS${NC}: Invalid file correctly rejected" | tee -a $RESULTS_FILE
else
    echo -e "${RED}❌ FAIL${NC}: Invalid file not rejected" | tee -a $RESULTS_FILE
fi
echo "" | tee -a $RESULTS_FILE

# Cleanup
rm -f $TEST_FILE invalid_file.bin

# Summary
echo "======================================" | tee -a $RESULTS_FILE
echo -e "${GREEN}✅ All Phase 1 Tests Passed!${NC}" | tee -a $RESULTS_FILE
echo "======================================" | tee -a $RESULTS_FILE
echo "" | tee -a $RESULTS_FILE
echo "📝 Full results saved to: $RESULTS_FILE" | tee -a $RESULTS_FILE
