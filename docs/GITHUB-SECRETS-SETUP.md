# Step-by-Step: Add GitHub Secrets

## 🛠️ Step 1: Add LIGHTSAIL_SSH_KEY

### Copy your SSH key:

```bash
# Display your Lightsail SSH key
cat /Users/karthiksankaran/MovieWeave/pem-key/MovieWeave-instance.pem
```

### Add to GitHub:

1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click **"New repository secret"**
3. **Name:** `LIGHTSAIL_SSH_KEY`
4. **Value:** Paste the entire key content (including `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----`)
5. Click **"Add secret"**

### Verify it works:

```bash
# Test SSH connection
ssh -i ~/.ssh/movieweave.pem ubuntu@34.204.47.202 "echo 'SSH access verified!'"
```

---

## 🛠️ Step 2: Add LIGHTSAIL_INSTANCE_IP

1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click **"New repository secret"**
3. **Name:** `LIGHTSAIL_INSTANCE_IP`
4. **Value:** `34.204.47.202`
5. Click **"Add secret"**

---

## 🛠️ Step 3: Add AWS Credentials (for S3)

### Create IAM User in AWS Console:

1. Go to **AWS Console** → **IAM** → **Users** → **Create user**
2. **Username:** `movieweave-github-actions`
3. **Console access:** NO (API only)
4. **Next:** Attach policies
5. Select: **AmazonS3FullAccess**
6. **Next:** Review and create
7. Click the new user
8. Go to **"Security credentials"** tab
9. Click **"Create access key"**
10. Select **"Application running on AWS resources"**
11. **Next:** Copy the values

### Add to GitHub Secrets:

**Secret #1 - Access Key ID:**
1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click **"New repository secret"**
3. **Name:** `AWS_ACCESS_KEY_ID`
4. **Value:** `AKIA...` (your access key ID)
5. Click **"Add secret"**

**Secret #2 - Secret Access Key:**
1. Click **"New repository secret"** again
2. **Name:** `AWS_SECRET_ACCESS_KEY`
3. **Value:** `wJalr...` (your secret key)
4. Click **"Add secret"**

⚠️ **Important:** Save these securely in 1Password/LastPass. AWS only shows them once!

---

## 🚀 How GitHub Actions Workflows Work

### 1. **Deploy Workflow** (auto-triggered on push to main)

**Triggered when:** You push to `main` branch

**What it does:**
1. ✅ Builds Docker image
2. ✅ Runs tests
3. ✅ Pushes image to GitHub Container Registry
4. ✅ Connects to Lightsail via SSH
5. ✅ Pulls latest code
6. ✅ Runs `docker-compose up -d`
7. ✅ Verifies health check

**Required secrets:** `LIGHTSAIL_SSH_KEY`, `LIGHTSAIL_INSTANCE_IP`

---

### 2. **Quality Checks Workflow** (auto-triggered on push/PR)

**Triggered when:** You push to `main`/`develop` or create PR

**What it does:**
1. ✅ Runs Flake8 linting
2. ✅ Checks code formatting with Black
3. ✅ Verifies import sorting with isort
4. ✅ Security scan with Bandit
5. ✅ Checks for vulnerable dependencies
6. ✅ Lints Dockerfile
7. ✅ Builds Docker image
8. ✅ Scans for exposed secrets

**Required secrets:** None

---

### 3. **Health Check Workflow** (auto-triggered every 6 hours)

**Triggered when:** Every 6 hours (automatic schedule)

**What it does:**
1. ✅ Pings MovieWeave API health endpoint
2. ✅ Checks S3 connectivity
3. ✅ Sends Slack notification if unhealthy

**Required secrets:** `LIGHTSAIL_INSTANCE_IP`

---

## ✅ Verify Setup

### Check if secrets are configured:

```bash
# Go to GitHub:
https://github.com/karlondon/MovieWeave/settings/secrets/actions
```

You should see all secrets listed (values hidden for security).

### Monitor workflow runs:

```bash
# Go to GitHub:
https://github.com/karlondon/MovieWeave/actions
```

Watch live progress as workflows run automatically.

---

## 🧪 Test Deployment

After adding secrets, trigger a test deployment:

```bash
# Make a change and push to main
cd /Users/karthiksankaran/MovieWeave
git add .
git commit -m "test: trigger GitHub Actions workflow"
git push origin main

# Watch the workflow run in GitHub Actions tab
# https://github.com/karlondon/MovieWeave/actions
```

---

## 🔧 Troubleshooting

### SSH key permission denied

**Solution:**
1. Verify `LIGHTSAIL_SSH_KEY` secret contains the full private key
2. Check SSH key starts with `-----BEGIN PRIVATE KEY-----`
3. Re-copy and paste the entire key

### Docker build fails in Actions

**Solution:**
1. Check if `docker/Dockerfile` exists
2. Verify Dockerfile is valid: `docker build -f docker/Dockerfile .`
3. Check GitHub Actions logs for specific error

### Deployment fails but tests pass

**Solution:**
1. Verify `LIGHTSAIL_INSTANCE_IP` is correct: `34.204.47.202`
2. Check if SSH key has permission: `ssh -i key.pem ubuntu@34.204.47.202`
3. Verify instance is running: `curl http://34.204.47.202:8000/health`

### "SSH: command not found" error

**Solution:**
1. Ensure `LIGHTSAIL_SSH_KEY` is properly formatted (multiline)
2. Check for extra spaces or line breaks
3. Verify key starts with `-----BEGIN PRIVATE KEY-----`
