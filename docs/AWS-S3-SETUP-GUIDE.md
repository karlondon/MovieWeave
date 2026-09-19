# AWS S3 Setup Guide for MovieWeave

## 📋 Overview

This guide walks you through creating an S3 bucket and configuring it for MovieWeave to store videos and backups.

**Prerequisites:**
- AWS account with console access
- GitHub secrets already configured (AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY)

---

## 🔧 STEP 1: Create S3 Bucket in AWS Console

### Navigate to S3

1. Go to: https://console.aws.amazon.com/s3/
2. Click **"Create bucket"** button

### Configure Bucket Settings

**Bucket name:**
```
movieweave-storage
```

**AWS Region:**
```
us-east-1
```
(Same as your Lightsail instance)

**Block Public Access Settings:**
```
✓ Check ALL boxes (Block all public access)
```

**Bucket Versioning:**
```
Disable (to save costs)
```

**Default encryption:**
```
Enable (AES-256)
```

### Create Bucket

Click **"Create bucket"** and wait for confirmation.

✅ Your S3 bucket is now created!

---

## 📊 STEP 2: Create Lifecycle Policy (Auto-Archive)

This saves money by moving old videos to cheaper storage automatically.

### Navigate to Lifecycle

1. Click your bucket: **movieweave-storage**
2. Go to **"Management"** tab
3. Click **"Create lifecycle rule"**

### Configure Rule

**Rule name:**
```


---

## 📝 STEP 5: Update Lightsail Configuration

Now update your `.env` file on the Lightsail instance with S3 settings.

### SSH into Lightsail

```bash
ssh -i /path/to/MovieWeave-instance.pem ubuntu@34.204.47.202

# Navigate to your app directory
cd /opt/movieweave

# Edit the .env file
nano .env
```

### Add S3 Configuration

Add or update these lines in your `.env`:

```env
# AWS S3 Configuration
AWS_S3_BUCKET=movieweave-storage
AWS_REGION=us-east-1
AWS_S3_ENABLED=true

# Storage paths
S3_UPLOAD_DIR=videos/uploads
S3_OUTPUT_DIR=videos/output
S3_BACKUP_DIR=backups
```

**Save the file:** Press `Ctrl+O`, then `Enter`, then `Ctrl+X`

### Restart Application

```bash
cd /opt/movieweave
docker-compose restart app

# Verify it's running
docker-compose logs -f app
```

---

## 🧪 STEP 6: Test S3 Connection

### Quick Test from Lightsail

```bash
ssh -i /path/to/MovieWeave-instance.pem ubuntu@34.204.47.202

# Test S3 access with Python
python3 << 'EOF'
import boto3
import os

try:
    s3_client = boto3.client('s3', region_name='us-east-1')
    response = s3_client.list_buckets()
    print("✅ S3 Authentication successful!")
    print(f"Buckets: {[b['Name'] for b in response['Buckets']]}")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

Expected output:
```
✅ S3 Authentication successful!
Buckets: ['movieweave-storage']
```

---

## 📊 STEP 7: Monitor S3 Usage & Costs

### Check Bucket Size

In AWS Console:
1. Go to S3 → **movieweave-storage**
2. Click **"Metrics"** tab
3. View bucket size and object count

### Cost Estimates

For **100GB** of videos with lifecycle policy:

| Period | Storage Class | Cost/Month |
|--------|--------------|-----------|
| Months 1-1 | Standard | $2.30 |
| Months 1-3 | Standard-IA | $1.25 |
| Months 3-12 | Glacier | $0.40 |
| After 1 year | Deleted | $0 |

**Annual cost:** ~$40 for 100GB (includes data transfer)

---

## ✅ YOUR S3 SETUP CHECKLIST

- [ ] S3 bucket created: `movieweave-storage` in `us-east-1`
- [ ] Bucket is **private** (all public access blocked)
- [ ] Lifecycle policy configured (auto-archive after 90 days)
- [ ] IAM policy created: `MovieWeave-S3-Access-Only`
- [ ] Policy attached to your GitHub Actions IAM user
- [ ] `.env` file on Lightsail updated with S3 settings
- [ ] Application restarted: `docker-compose restart app`
- [ ] S3 connection test successful

---

## 🚀 NEXT: Deploy with S3 Integration

Once S3 is set up:

```bash
# On your local machine
cd /Users/karthiksankaran/MovieWeave

# Push a commit to trigger deployment
git add .
git commit -m "feat: enable S3 integration"
git push origin main
```

GitHub Actions will automatically deploy your app with full S3 support!

---

## 🔗 USEFUL LINKS

| Link | Purpose |
|------|---------|
| https://console.aws.amazon.com/s3/ | S3 Console |
| https://console.aws.amazon.com/iam/ | IAM Console |
| https://console.aws.amazon.com/billing/ | Billing Console |

**You're all set with S3!** 🎉

archive-old-videos
```

**Check these:**
- ✓ Transition current versions between storage classes
- ✓ Expire current versions

**Transitions:**
- After **30 days** → **Standard-IA** (45% cheaper)
- After **90 days** → **Glacier** (83% cheaper)

**Expiration:**
- After **365 days** → Delete automatically

Click **"Create rule"**

**Cost Savings:** Videos automatically get cheaper to store over time! 💰

---

## 🔐 STEP 3: Create IAM Policy

This restricts permissions - security best practice!

### Navigate to IAM

1. Go to: https://console.aws.amazon.com/iam/
2. Click **"Policies"** 
3. Click **"Create policy"**

### Create Custom Policy

**Name:**
```
MovieWeave-S3-Access-Only
```

**Click "JSON" tab and paste:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::movieweave-storage",
        "arn:aws:s3:::movieweave-storage/*"
      ]
    }
  ]
}
```

Click **"Next"** → **"Create policy"**

---

## 👤 STEP 4: Attach Policy to Your GitHub Actions User

### Find Your User

1. Go to: https://console.aws.amazon.com/iam/
2. Click **"Users"**
3. Find your user (named something like `movieweave-github-actions`)

### Attach Policy

1. Click on the user name
2. Go to **"Permissions"** tab
3. Click **"Add permissions"** → **"Attach policies directly"**
4. Search for: `MovieWeave-S3-Access-Only`
5. ✓ Check the box
6. Click **"Add permissions"**

✅ Your user now has S3 bucket access!
