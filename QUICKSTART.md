# 🎬 MovieWeave Quick Start Guide

## 📦 Project Structure

```
MovieWeave/
├── README.md                    (Project overview)
├── .env.example                 (Environment template)
├── docker-compose.yml           (Service orchestration)
├── pem-key/                     (SSH keys - add your key here)
├── backend/                     (FastAPI application)
├── docker/                      (Docker configuration)
├── config/                      (Nginx & environment)
├── scripts/                     (Deployment scripts)
└── docs/                        (Documentation)
```

## 🚀 Quick Start (5 Steps)

### Step 1: Add Your SSH Key
```bash
# Copy your MovieWeave Lightsail SSH key to:
/Users/karthiksankaran/PS-Scripts/MovieWeave/pem-key/movieweave.pem

chmod 600 /Users/karthiksankaran/PS-Scripts/MovieWeave/pem-key/movieweave.pem
```

### Step 2: Connect to Instance
```bash
ssh -i /Users/karthiksankaran/PS-Scripts/MovieWeave/pem-key/movieweave.pem \
    ubuntu@34.204.47.202
```

### Step 3: Run Initial Setup
```bash
# On the instance:
cd /opt/movieweave
sudo bash scripts/initial-setup.sh
```

**Installs:** Docker, Python 3.11, FFmpeg, Nginx, Node.js, AWS CLI, Firewall, Swap

### Step 4: Configure Environment
```bash
nano .env

# Required settings:
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=movieweave-storage
```

### Step 5: Deploy
```bash
bash scripts/deploy.sh
```

## ✅ Verify Setup

```bash
# Check services
docker-compose ps

# View logs
docker-compose logs -f

# Test API
curl http://localhost:8000/health

# API docs: http://34.204.47.202:8000/docs
```
