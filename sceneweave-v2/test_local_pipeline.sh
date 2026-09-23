#!/bin/bash
# test_local_pipeline.sh - Test end-to-end pipeline locally

set -e

API_URL="http://localhost:8000"
STORY_FILE="/tmp/detective_story.txt"

echo "🎬 SceneWeave End-to-End Test"
echo "=============================="
echo ""

# Create test story
echo "📝 Creating test story..."
cat > "$STORY_FILE" << 'EOF'
Brianna was hovering on the threshold of sleep when Detective Raccoon climbed up onto the bed. 
"It's past my bedtime," Brianna yawned. "Apologies, mademoiselle," said Detective Raccoon. 
"I am afraid this matter cannot wait." Brianna sat up. "Is this about the princess?" 
Detective Raccoon said, "The princess has disappeared." "The cat did it," said Brianna. 
"Do not make assumptions, mon petit!" warned Detective Raccoon. "Well? Am I a damsel or a monster?" 
Brianna asked. "There is still time to rescue her," said Detective Raccoon. 
Brianna climbed out of bed, determined to put things right. That is what heroes do.
EOF
echo "✅ Story created"
echo ""

# Test 1: Health check
echo "1️⃣ Testing API Health..."
if curl -s "$API_URL/api/health" | grep -q "healthy"; then
    echo "✅ API is healthy"
else
    echo "❌ API is not responding. Make sure backend is running:"
    echo "   python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"
    exit 1
fi
echo ""

# Test 2: Upload story
echo "2️⃣ Uploading story..."
RESPONSE=$(curl -s -X POST "$API_URL/api/upload" \
  -F "file=@$STORY_FILE")

JOB_ID=$(echo "$RESPONSE" | grep -o '"job_id":"[^"]*' | cut -d'"' -f4)

if [ -z "$JOB_ID" ]; then
    echo "❌ Upload failed"
    echo "Response: $RESPONSE"
    exit 1
fi

echo "✅ Story uploaded"
echo "   Job ID: $JOB_ID"
echo ""

# Test 3: Check status
echo "3️⃣ Monitoring job progress..."
for i in {1..30}; do
    STATUS=$(curl -s "$API_URL/api/status/$JOB_ID" | grep -o '"status":"[^"]*' | cut -d'"' -f4)
    PROGRESS=$(curl -s "$API_URL/api/status/$JOB_ID" | grep -o '"progress":[0-9]*' | cut -d':' -f2)
    
    echo "   [Attempt $i/30] Status: $STATUS | Progress: $PROGRESS%"
    
    if [ "$STATUS" = "COMPLETE" ]; then
        echo "✅ Job completed!"
        break
    elif [ "$STATUS" = "FAILED" ]; then
        echo "❌ Job failed"
        exit 1
    fi
    
    sleep 2
done
echo ""

# Test 4: Download video
echo "4️⃣ Downloading video..."
OUTPUT_FILE="/tmp/sceneweave_output.mp4"

if curl -s "$API_URL/api/download/$JOB_ID" -o "$OUTPUT_FILE"; then
    FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
    echo "✅ Video downloaded: $OUTPUT_FILE ($FILE_SIZE)"
else
    echo "❌ Download failed"
    exit 1
fi
echo ""

# Test 5: List all jobs
echo "5️⃣ Listing all jobs..."
JOBS=$(curl -s "$API_URL/api/jobs" | grep -o '"job_id":"[^"]*' | wc -l)
echo "✅ Total jobs: $JOBS"
echo ""

echo "=============================="
echo "✅ ALL TESTS PASSED!"
echo "=============================="
echo ""
echo "📺 To view the video:"
echo "   open $OUTPUT_FILE"
echo ""
echo "🌐 To use the web UI:"
echo "   npm start  (in frontend directory)"
echo ""
echo "🚀 To deploy to Lightsail:"
echo "   bash deploy_to_lightsail.sh"
