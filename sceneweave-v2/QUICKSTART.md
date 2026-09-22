# 🚀 SceneWeave MVP - Quick Start Guide

## Prerequisites

- Python 3.10+
- pip and venv
- ~2GB disk space

## Installation (5 minutes)

### 1. Navigate to Project
```bash
cd /Users/karthiksankaran/MovieWeave/sceneweave-v2/backend
```

### 2. Create Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment
```bash
cp ../.env.example .env
# Edit if needed: nano .env
```

### 5. Run Backend
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ **Backend ready at:** `http://localhost:8000`  
📚 **API Docs:** `http://localhost:8000/docs`

---

## Testing Phase 1

### Test 1: Health Check
```bash
curl http://localhost:8000/api/health
```

Expected:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2026-09-22T12:00:00"
}
```

### Test 2: Upload File
```bash
echo "Once upon a time, there was a brave knight." > test.txt
curl -X POST -F "file=@test.txt" http://localhost:8000/api/upload
```

Expected:
```json
{
  "job_id": "550e8400-...",
  "filename": "test.txt",
  "status": "pending",
  "message": "File uploaded successfully...",
  "timestamp": "2026-09-22T12:00:00"
}
```

### Test 3: Check Job Status
```bash
# Replace with actual job_id from Test 2
curl http://localhost:8000/api/status/550e8400-...
```

### Test 4: List All Jobs
```bash
curl http://localhost:8000/api/jobs
```

---

## Next: Phase 2 - Ollama Integration

Once you confirm Phase 1 works, I'll implement:
- Ollama LLM script generation
- Structured JSON dialogue output
- Progress tracking for script generation
