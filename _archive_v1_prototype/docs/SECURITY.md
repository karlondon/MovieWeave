# 🔐 MovieWeave SSH Key Security Guide

## ⚠️ CRITICAL: Protect Your SSH Key!

Your MovieWeave SSH key is **extremely sensitive**. It grants full access to your AWS Lightsail instance.

## ✅ Security Setup Complete

### What Has Been Done:

1. **`.gitignore` Created** ✅
   - All `*.pem` files ignored (SSH keys)
   - `.env` files ignored (credentials)
   - AWS credentials ignored
   - Database files ignored

2. **File Structure Protected** ✅
   - `pem-key/` folder structure preserved
   - Contents never committed to Git
   - Safe to push to GitHub/GitLab

## 📋 Setup Instructions

### Step 1: Verify `.gitignore` is working
```bash
cd /Users/karthiksankaran/PS-Scripts/MovieWeave
git check-ignore -v pem-key/*.pem
# Should output that .pem files are ignored
```

### Step 2: Set Proper File Permissions

```bash
# Set SSH key permissions (600 = read/write for owner only)
chmod 600 /Users/karthiksankaran/PS-Scripts/MovieWeave/pem-key/*.pem

# Restrict directory (700 = full access for owner only)
chmod 700 /Users/karthiksankaran/PS-Scripts/MovieWeave/pem-key/

# Verify (should show: -rw-------)
ls -la /Users/karthiksankaran/PS-Scripts/MovieWeave/pem-key/
```

### Step 3: Never Do These Things ⛔

```bash
# ❌ DON'T: Commit SSH key to Git
git add pem-key/movieweave.pem

# ❌ DON'T: Share via email/chat/Slack/Discord
# ❌ DON'T: Upload to public cloud storage
# ❌ DON'T: Include in screenshots
```

## ✅ Do These Things Instead

```bash
# ✅ DO: Keep SSH key on local machine only
# ✅ DO: Use chmod 600 on the file
# ✅ DO: Use chmod 700 on the directory
# ✅ DO: Back it up to 1Password or LastPass
# ✅ DO: Use Git to backup other files safely
```

## 💾 Backup Your SSH Key Securely

### Option 1: 1Password (Recommended)
```bash
# Add your SSH key to 1Password vault:
# 1. Open 1Password
# 2. Create "Secure Note" or "SSH Key" entry
# 3. Copy contents of movieweave.pem
# 4. Store encrypted in your 1Password vault
# 5. Delete local copy if extra safety needed
```

### Option 2: LastPass
```bash
# Similar to 1Password:
# - Create secure note
# - Paste SSH key contents
# - Encrypt with master password
```

### Option 3: Encrypted USB Drive
```bash
# For offline backup:
# - Copy pem-key/ to encrypted USB
# - Store in safe location
# - Keep as backup only
```

## 🚨 If Your Key is Compromised

### Immediately:

1. **Stop the instance** (AWS Console)
2. **Create new instance** with new SSH key
3. **Never use old key again**

## 📝 What `.gitignore` Protects

```
✅ PROTECTED (will NOT commit):
├── pem-key/*.pem           (SSH keys)
├── .env                    (AWS credentials)
├── credentials             (AWS config)
├── data/jobs_db.json       (job data)
└── logs/                   (application logs)

✅ SAFE (WILL commit - no secrets):
├── README.md               (documentation)
├── docker-compose.yml      (configuration)
├── backend/main.py         (application code)
├── scripts/*.sh            (automation)
└── docs/                   (documentation)
```
