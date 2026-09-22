# MovieWeave Feature 3 - REST API Documentation

## API Endpoints

### 1. Health Check
```
GET /api/health

Response (200 OK):
{
  "status": "healthy",
  "version": "3.0.0"
}
```

### 2. Get All Characters
```
GET /api/characters

Response (200 OK):
{
  "success": true,
  "count": 10,
  "characters": ["hero_001", "hero_002", ..., "hero_010"]
}
```

### 3. Get Character Details
```
GET /api/characters/{character_name}

Response (200 OK):
{
  "success": true,
  "name": "hero_001",
  "expressions": ["neutral", "happy", "sad", "angry"],
  "mouths": ["A", "E", "I", "O", "U", "MBP", "X"]
}
```

### 4. Generate Video (Core Endpoint)
```
POST /api/video/generate

Request (JSON):
{
  "character_name": "hero_001",  ✓ Required
  "expression": "happy",          ✓ Required
  "duration": 3.0,                ✓ Required (0.5-60 sec)
  "audio": <file>                 ✗ Optional (MP3/WAV/AAC)
}

Response (200 OK):
{
  "success": true,
  "message": "Video generated successfully",
  "video_file": "hero_001_happy_20260921_143022.mp4",
  "duration": 3.0,
  "character": "hero_001",
  "expression": "happy"
}

Processing time: 3-6 seconds per video
```

### 5. Download Video
```
GET /api/video/{filename}

Response: Binary MP4 video file
```

## CURL Examples

```bash
# Check health
curl http://localhost:5000/api/health

# List characters
curl http://localhost:5000/api/characters

# Get character info
curl http://localhost:5000/api/characters/hero_001

# Generate video
curl -X POST http://localhost:5000/api/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "character_name": "hero_001",
    "expression": "happy",
    "duration": 3.0
  }'

# Generate with audio
curl -X POST http://localhost:5000/api/video/generate \
  -F "character_name=hero_001" \
  -F "expression=happy" \
  -F "duration=3.0" \
  -F "audio=@dialogue.mp3"

# Download video
curl -O http://localhost:5000/api/video/hero_001_happy_20260921_143022.mp4
```

## Python Examples

```python
import requests

# Check health
requests.get('http://localhost:5000/api/health').json()

# Get characters
chars = requests.get('http://localhost:5000/api/characters').json()['characters']

# Generate video
data = {
    'character_name': 'hero_001',
    'expression': 'happy',
    'duration': 3.0
}
result = requests.post('http://localhost:5000/api/video/generate', json=data).json()
print(f"Video: {result['video_file']}")

# Generate with audio
files = {'audio': open('dialogue.mp3', 'rb')}
data = {
    'character_name': 'hero_001',
    'expression': 'neutral',
    'duration': 5.0
}
result = requests.post('http://localhost:5000/api/video/generate', 
                       data=data, files=files).json()
```

## JavaScript Examples

```javascript
// Get characters
fetch('/api/characters')
  .then(r => r.json())
  .then(d => console.log(d.characters));

// Generate video
const data = {
  character_name: 'hero_001',
  expression: 'happy',
  duration: 3.0
};
fetch('/api/video/generate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(data)
})
.then(r => r.json())
.then(d => console.log(d.video_file));

// Generate with audio
const formData = new FormData();
formData.append('character_name', 'hero_001');
formData.append('expression', 'happy');
formData.append('duration', 3.0);
formData.append('audio', audioFile);

fetch('/api/video/generate', {
  method: 'POST',
  body: formData
})
.then(r => r.json())
.then(d => {
  console.log('Video:', d.video_file);
  document.getElementById('video').src = `/api/video/${d.video_file}`;
});
```
