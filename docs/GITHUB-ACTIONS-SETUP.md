# GitHub Secrets Setup Guide for MovieWeave CI/CD

This guide walks you through configuring all required GitHub Secrets for the automated deployment pipeline.

## 🔐 Required Secrets

### 1. **LIGHTSAIL_SSH_KEY** (Required for Deployment)
Private SSH key for accessing your Lightsail instance

**How to add:**
1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click "New repository secret"
3. Name: `LIGHTSAIL_SSH_KEY`
4. Value: Copy-paste the contents of your Lightsail PEM file

**To get your SSH key:**
```bash
cat /Users/karthiksankaran/MovieWeave/pem-key/MovieWeave-instance.pem
```

---

### 2. **LIGHTSAIL_INSTANCE_IP** (Required for Deployment)
Public IP address of your MovieWeave Lightsail instance

**Value:** `34.204.47.202`

**How to add:**
1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click "New repository secret"
3. Name: `LIGHTSAIL_INSTANCE_IP`
4. Value: `34.204.47.202`

---

### 3. **AWS_ACCESS_KEY_ID** (Required for S3 Integration)
IAM user access key for AWS S3 bucket access

**How to get:**
1. Go to AWS Console → IAM → Users
2. Create new user: `movieweave-github-actions`
3. Attach policy: `AmazonS3FullAccess`
4. Generate access keys
5. Copy the Access Key ID

---

### 4. **AWS_SECRET_ACCESS_KEY** (Required for S3 Integration)
IAM user secret access key

**How to get:**
1. Same IAM user as above
2. Copy the Secret Access Key (shown only once!)
3. Save it securely in 1Password/LastPass

---

### 5. **SLACK_WEBHOOK_URL** (Optional - For Notifications)
Slack webhook for deployment and health check notifications

**How to get:**
1. Go to your Slack Workspace Settings
2. Create Incoming Webhook
3. Copy the webhook URL

**Status:** ⏳ Optional - Add later if you use Slack

---

### 6. **GITGUARDIAN_API_KEY** (Optional - For Secret Scanning)
API key for GitGuardian secret detection

**Status:** ⏳ Optional - Add if you want secret scanning

---

## 📋 Quick Setup Checklist

### ✅ MINIMUM REQUIRED (to get CI/CD working):

- [ ] `LIGHTSAIL_SSH_KEY` - Your Lightsail private SSH key
- [ ] `LIGHTSAIL_INSTANCE_IP` - IP address: `34.204.47.202`

### 📦 RECOMMENDED (for S3 integration):

- [ ] `AWS_ACCESS_KEY_ID` - From IAM user
- [ ] `AWS_SECRET_ACCESS_KEY` - From IAM user

### 🎁 OPTIONAL (nice-to-have):

- [ ] `SLACK_WEBHOOK_URL` - For deployment notifications
- [ ] `GITGUARDIAN_API_KEY` - For security scanning
