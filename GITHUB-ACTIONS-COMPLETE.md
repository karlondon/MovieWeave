# 🎉 MovieWeave GitHub Actions Setup - COMPLETE

## ✅ What Has Been Done

### 1. ✅ GitHub Repository Initialized
- **Repository:** https://github.com/karlondon/MovieWeave
- **Branch:** `main`
- **Initial commit:** Pushed with all project files and GitHub Actions workflows
- **SSH authentication:** Configured and tested successfully

### 2. ✅ GitHub Actions Workflows Created

Three automated CI/CD workflows have been created:

#### **A. Deploy Workflow** (`.github/workflows/deploy.yml`)
- **Triggers:** On every push to `main` branch
- **What it does:**
  - ✅ Builds Docker image from `docker/Dockerfile`
  - ✅ Runs code quality checks
  - ✅ Pushes Docker image to GitHub Container Registry
  - ✅ Connects to Lightsail via SSH (using `LIGHTSAIL_SSH_KEY` secret)
  - ✅ Pulls latest code on instance
  - ✅ Runs `docker-compose up -d` to start services
  - ✅ Verifies health check at `http://34.204.47.202:8000/health`
- **Duration:** ~5-10 minutes per deployment
- **Status:** ⏳ Ready, awaiting secrets configuration

#### **B. Quality Checks Workflow** (`.github/workflows/quality-checks.yml`)
- **Triggers:** On every push and pull request
- **What it does:** Flake8, Black, isort, Bandit, Docker lint
- **Duration:** ~3-5 minutes
- **Status:** ✅ Ready to use (no secrets required)

#### **C. Health Check Workflow** (`.github/workflows/health-check.yml`)
- **Triggers:** Every 6 hours automatically
- **What it does:** Pings API, checks database, verifies S3
- **Duration:** ~1 minute
- **Status:** ⏳ Ready, needs `LIGHTSAIL_INSTANCE_IP` secret

---

## 📋 GitHub Secrets You MUST Add NOW

Navigate to: **https://github.com/karlondon/MovieWeave/settings/secrets/actions**

### ⚠️ MINIMUM REQUIRED (2 secrets - takes 5 minutes):

#### **Secret 1: LIGHTSAIL_SSH_KEY**

Get your SSH key:
```bash
cat /Users/karthiksankaran/MovieWeave/pem-key/MovieWeave-instance.pem
```

Add to GitHub:
1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click "New repository secret"
3. **Name:** `LIGHTSAIL_SSH_KEY`
4. **Value:** Paste entire key (BEGIN to END lines)
5. Click "Add secret"

#### **Secret 2: LIGHTSAIL_INSTANCE_IP**

Add to GitHub:
1. Click "New repository secret"
2. **Name:** `LIGHTSAIL_INSTANCE_IP`
3. **Value:** `34.204.47.202`
4. Click "Add secret"

### 📦 RECOMMENDED (for S3):

- **`AWS_ACCESS_KEY_ID`** - Get from AWS IAM user
- **`AWS_SECRET_ACCESS_KEY`** - Get from AWS IAM user

---

## 🚀 Your Action Items (in order):

### **#1: Add 2 GitHub Secrets (5 minutes)**
- [ ] `LIGHTSAIL_SSH_KEY` - Copy from `/Users/karthiksankaran/MovieWeave/pem-key/`
- [ ] `LIGHTSAIL_INSTANCE_IP` - Set to `34.204.47.202`

### **#2: Prepare Lightsail Instance (10 minutes)**
```bash
ssh -i /path/to/MovieWeave-instance.pem ubuntu@34.204.47.202
sudo mkdir -p /opt/movieweave
sudo chown ubuntu:ubuntu /opt/movieweave
cd /opt/movieweave
git clone https://github.com/karlondon/MovieWeave.git .
mkdir -p data/uploads data/output data/temp
cp .env.example .env
nano .env  # Edit with your AWS credentials
```

### **#3: Test Deployment (2 minutes)**
```bash
cd /Users/karthiksankaran/MovieWeave
git add .
git commit -m "test: trigger GitHub Actions"
git push origin main
```

Watch at: https://github.com/karlondon/MovieWeave/actions

### **#4: Verify It Works (1 minute)**
```bash
curl http://34.204.47.202:8000/health
```

---

## ✅ After This - What's Automatic

**Every push to `main` from now on automatically:**
1. Runs code quality checks (~3 min)
2. Builds Docker image (~5 min)
3. Deploys to Lightsail (~3 min)
4. Verifies health (~1 min)
5. Total: ~12 minutes from push to production

**Every 6 hours automatically:**
- Health check pings your API
- Notifies you if anything fails

---

## 📞 You're Ready!

All GitHub Actions workflows are set up and live. Just add the 2 required secrets and you'll have fully automated CI/CD! 🚀

