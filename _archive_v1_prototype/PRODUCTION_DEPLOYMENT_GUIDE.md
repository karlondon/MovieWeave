# MovieWeave v4.0 - Production Deployment

## 🚀 QUICKEST DEPLOYMENT (Docker Compose)

```bash
cd /tmp/MovieWeave
docker-compose up -d
```

**That's it! Your app is running:**
- Dashboard: http://localhost:5000
- API: http://localhost:5000/api/health

## 📋 Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| Web | 5000 | Flask application |
| Redis | 6379 | Cache & broker |
| Celery | - | Background tasks |
| Nginx | 80/443 | Reverse proxy |

## 🐧 Linux/Ubuntu Deployment

```bash
bash deploy_production.sh movieweave.example.com 5000 4
```

**Installs & configures:**
- Python 3.9 + FFmpeg
- Gunicorn (4 workers)
- Nginx + SSL
- Supervisor process manager
- Redis cache

## ☁️ Cloud Deployment

**AWS EC2:**
```bash
# Launch Ubuntu 20.04 t3.medium instance
ssh -i key.pem ubuntu@your-ip
git clone <repo>
cd MovieWeave
bash deploy_production.sh yourdomain.com 5000 4
```

**Google Cloud Run:**
```bash
gcloud run deploy movieweave --source .
```

**Heroku:**
```bash
heroku create movieweave
git push heroku main
```

## 🔒 Security Checklist

- ✅ HTTPS/SSL enabled (auto with script)
- ✅ Firewall configured (ports 80, 443)
- ✅ Input validation
- ✅ File upload limits
- ✅ Process isolation

## 📊 Production Architecture

```
Client → Nginx (reverse proxy) → Gunicorn (4 workers)
                                     ↓
                         Flask + Features 1-4
                                     ↓
                    Redis + Celery ← File Storage
```

## ⚙️ Management Commands

```bash
# Docker
docker-compose ps              # Status
docker-compose logs -f web     # Logs
docker-compose restart web     # Restart

# Linux/Supervisor
sudo supervisorctl status
sudo supervisorctl restart movieweave
sudo tail -f /opt/movieweave/logs/error.log
```

## 📈 Scaling

**Single server:** 50-100 concurrent users  
**Multiple servers:** Add load balancer + Redis + S3 storage

---

**MovieWeave v4.0 is production-ready!** 🎬
