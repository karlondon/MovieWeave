# 🚀 SceneWeave MVP - Production Deployment to Lightsail

## Production Server

| Item | Value |
|------|-------|
| **IP** | `34.204.47.202` |
| **API** | `http://34.204.47.202:8000` |
| **Docs** | `http://34.204.47.202:8000/docs` |
| **Project** | `/home/ubuntu/sceneweave-v2` |
| **Data** | `/data/sceneweave` |

---

## 🚀 Deploy in 1 Command

```bash
cd /Users/karthiksankaran/MovieWeave/sceneweave-v2
bash deploy_to_lightsail.sh
```

This automatically:
- ✅ Verifies SSH connectivity
- ✅ Creates remote directories
- ✅ Transfers code via rsync
- ✅ Sets up Python environment
- ✅ Installs dependencies
- ✅ Creates systemd service
- ✅ Starts API server
- ✅ Verifies API health

---

## 🛠️ Management Commands

```bash
./manage_lightsail.sh status      # View service status
./manage_lightsail.sh logs        # Tail live logs
./manage_lightsail.sh restart     # Restart service
./manage_lightsail.sh health      # Check API health
./manage_lightsail.sh ssh         # SSH into server
```

---

## 🧪 Test Production API

```bash
# Automated testing
./test_production.sh

# Manual tests
curl http://34.204.47.202:8000/api/health
curl http://34.204.47.202:8000/api/jobs
```

---

## 📝 Files on Lightsail

```
/home/ubuntu/sceneweave-v2/    ← Project code
/data/sceneweave/              ← Data (uploads, logs, outputs)
  ├── uploads/
  ├── output/
  ├── temp/
  └── logs/
```

---

## ✅ Verify Deployment Works

1. Run: `bash deploy_to_lightsail.sh`
2. Wait for completion (should take 2-3 minutes)
3. See green ✅ checkmarks
4. Open browser: `http://34.204.47.202:8000/docs`
5. Try uploading a file or checking health

All done! No more localhost. Everything runs on Lightsail.
