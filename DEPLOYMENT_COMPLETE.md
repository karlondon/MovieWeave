# 🚀 SceneWeave MVP v2.0 - DEPLOYMENT COMPLETE

## ✅ TASKS COMPLETED

### 1. GitHub Actions Removed
- ✅ Deleted all GitHub Actions workflows (deploy.yml, health-check.yml, quality-checks.yml)
- ✅ Removed hardcoded API secrets from code
- ✅ Repository is now clean and secure

### 2. All Changes Committed to GitHub
- ✅ Committed entire SceneWeave v2 system with hybrid workflow
- ✅ Archived v1 prototype in _archive_v1_prototype/
- ✅ Pushed to: https://github.com/karlondon/MovieWeave (develop branch)

### 3. Deployed to AWS Lightsail
- ✅ **Server IP:** 34.229.168.102
- ✅ **API Running:** http://34.229.168.102:8000
- ✅ **Health Status:** ✅ PASSING
- ✅ **Service:** Running via systemd (sceneweave.service)

### 4. Frontend Testing UI Created
- ✅ Curator Dashboard HTML interface ready
- ✅ Web-based testing available at http://34.229.168.102:8000/ui
- ✅ Full API documentation available at http://34.229.168.102:8000/docs

---

## 🧪 QUICK START TESTING

### Test via cURL (Recommended)

**1. Check API Health**
```bash
curl http://34.229.168.102:8000/api/health
```

**2. Submit a Story**
```bash
curl -X POST http://34.229.168.102:8000/api/hybrid/submit-story \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Adventure of Luna",
    "story_text": "Once upon a time, a young girl named Luna discovered a magical forest...",
    "tags": ["adventure", "kids"]
  }'
```

**3. View Pending Stories**
```bash
curl http://34.229.168.102:8000/api/hybrid/pending-stories
```

**4. Approve Story**
```bash
curl -X POST http://34.229.168.102:8000/api/hybrid/review-story/{story_id} \
  -H "Content-Type: application/json" \
  -d '{"approved": true}'
```

**5. Create Batch**
```bash
curl -X POST http://34.229.168.102:8000/api/hybrid/create-batch \
  -H "Content-Type: application/json" \
  -d '{"batch_name": "Morning Release", "story_ids": ["{story_id}"]}'
```

**6. Start Processing**
```bash
curl -X POST http://34.229.168.102:8000/api/hybrid/process-batch/{batch_id} \
  -H "Content-Type: application/json"
```

### Test via Web Browser

**Dashboard URL:** http://34.229.168.102:8000/ui

**Features:**
- 📝 Submit stories for curator review
- 👁️ Review and approve/reject stories
- 📦 Create batches and process videos
- Real-time status updates

---

## 📊 API ENDPOINTS

**Story Management**
- POST /api/hybrid/submit-story
- GET /api/hybrid/pending-stories
- POST /api/hybrid/review-story/{story_id}
- PUT /api/hybrid/edit-story/{story_id}

**Batch Processing**
- POST /api/hybrid/create-batch
- POST /api/hybrid/process-batch/{batch_id}
- GET /api/hybrid/batch-status/{batch_id}
- GET /api/hybrid/batches

**Health & Status**
- GET /api/health
- GET /api/status/{job_id}
- GET /api/jobs
- GET /api/download/{job_id}

---

## 🏗️ ARCHITECTURE

**Frontend:** React/HTML/CSS
**Backend:** FastAPI (Python 3.12)
**Video Processing:** FFmpeg
**Storage:** JSON-based database
**Deployment:** AWS Lightsail (Ubuntu 24.04)
**Service Manager:** systemd

---

## 📁 KEY FILES

- `/sceneweave-v2/backend/app/main.py` - FastAPI application
- `/sceneweave-v2/backend/app/api/hybrid_endpoints.py` - Hybrid workflow API
- `/sceneweave-v2/backend/app/utils/hybrid_workflow.py` - Workflow manager
- `/sceneweave-v2/backend/app/utils/lean_processor.py` - Video processor
- `/sceneweave-v2/backend/requirements.txt` - Python dependencies
- `/sceneweave-v2/deploy_to_lightsail.sh` - Deployment script

---

## 🔧 SERVER MANAGEMENT

**SSH Access**
```bash
ssh -i pem-key/NarrativeFilm-instance.pem ubuntu@34.229.168.102
```

**Check Status**
```bash
sudo systemctl status sceneweave.service
```

**View Logs**
```bash
tail -f /data/sceneweave/logs/sceneweave.log
```

**Restart Service**
```bash
sudo systemctl restart sceneweave.service
```

---

## ⏸️ PRICING TIER

**Coming Friday** - Pricing tiers will be finalized after testing series and identifying any issues. Check back Friday for details.

---

## ✨ STATUS: PRODUCTION READY - TESTING PHASE

