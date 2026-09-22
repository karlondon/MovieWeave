# MovieWeave: Complete Deployment Guide

## 🚀 Quick Start - From Zero to Production

This guide takes you through setting up MovieWeave with GitHub Actions for automated deployment.

## 📋 Prerequisites Checklist

Before starting, you should have:

- ✅ GitHub repository: https://github.com/karlondon/MovieWeave
- ✅ Lightsail instance: `34.204.47.202`
- ✅ SSH access to Lightsail
- ✅ AWS account with IAM access
- ✅ Docker installed (optional, for local testing)

---

## 🔐 STEP 1: Configure GitHub Secrets (5 minutes)

### 1.1 Add SSH Key Secret

```bash
# Copy your Lightsail SSH key
cat /Users/karthiksankaran/MovieWeave/pem-key/MovieWeave-instance.pem
```

1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click **"New repository secret"**
3. **Name:** `LIGHTSAIL_SSH_KEY`
4. **Value:** Paste entire key (including BEGIN/END lines)
5. Click **"Add secret"**

### 1.2 Add Instance IP Secret

1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click **"New repository secret"**
3. **Name:** `LIGHTSAIL_INSTANCE_IP`
4. **Value:** `34.204.47.202`
5. Click **"Add secret"**

### 1.3 Add AWS Credentials (Optional - for S3)

**Only if you want S3 integration for video storage.**

In AWS Console:
1. Go to **IAM** → **Users** → **Create user**
2. Username: `movieweave-github-actions`
3. Attach: **AmazonS3FullAccess**
4. Generate access keys

Then add GitHub secrets:
1. **`AWS_ACCESS_KEY_ID`** = your access key
2. **`AWS_SECRET_ACCESS_KEY`** = your secret key

---

## 🔧 STEP 2: Prepare Lightsail Instance (10 minutes)

SSH into your instance and set up deployment directories:

```bash
# Connect to Lightsail
ssh -i /path/to/your/ssh/key.pem ubuntu@34.204.47.202

# Create application directory
sudo mkdir -p /opt/movieweave
sudo chown ubuntu:ubuntu /opt/movieweave

# Clone repository
cd /opt/movieweave
git clone https://github.com/karlondon/MovieWeave.git .

# Create data directories
mkdir -p data/uploads data/output data/temp

# Copy environment configuration
cp .env.example .env
nano .env
```

### Key .env Settings for Lightsail:

```env
AWS_ACCESS_KEY_ID=your_actual_access_key
AWS_SECRET_ACCESS_KEY=your_actual_secret_key
AWS_S3_BUCKET=movieweave-storage
APP_ENV=production
DEBUG=false
ALLOWED_HOSTS=34.204.47.202,movieweave.example.com
```

---

## 📦 STEP 3: Test GitHub Actions Workflow

### Push Your First Commit:

```bash
cd /Users/karthiksankaran/MovieWeave
git add .
git commit -m "Initial commit: Set up GitHub Actions workflows"
git push origin main
```

### Watch the Workflow:

1. Go to: https://github.com/karlondon/MovieWeave/actions
2. Click the latest workflow run
3. Watch jobs execute in real-time

### Verify Deployment:

```bash
curl http://34.204.47.202:8000/health
```

You should see: `{"status": "ok"}`

---

## 🚀 STEP 4: Automated Deployments from Now On

**Every push to `main` automatically:**

1. ✅ Runs tests
2. ✅ Builds Docker image
3. ✅ Deploys to Lightsail
4. ✅ Runs health checks

**All automated via GitHub Actions!**

---

## ✅ Deployment Checklist

- [ ] GitHub secrets configured (SSH key & IP)
- [ ] Lightsail instance prepared
- [ ] `.env` file created on Lightsail
- [ ] First git push made
- [ ] GitHub Actions workflow ran successfully
- [ ] API health check passes

**You're ready to deploy!** 🚀
