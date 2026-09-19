# 📋 PHASE 5: Update Lightsail Instance - QUICK GUIDE

## What This Does

Updates your Lightsail instance's `.env` file with S3 configuration so your app can connect to and use S3.

---

## 🔧 STEP-BY-STEP

### 1. SSH into Lightsail

From your local machine, run:

```bash
ssh -i /path/to/MovieWeave-instance.pem ubuntu@34.204.47.202
```

Replace `/path/to/MovieWeave-instance.pem` with the actual path to your SSH key.

**Expected output:**
```
Welcome to Ubuntu 22.04 LTS
ubuntu@ip-172-26-xx-xxx:~$
```

### 2. Navigate to App Directory

```bash
cd /opt/movieweave
```

You should see your application files here.

### 3. View Current .env File

```bash
cat .env
```

This shows you what's currently configured.

### 4. Edit the .env File

```bash
nano .env
```

This opens the text editor.

### 5. Scroll to the End

Press **Ctrl+End** to go to the end of the file.

### 6. Add S3 Configuration

Add these lines at the end:

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

### 7. Save the File

Press: **Ctrl+O** (write out)
Press: **Enter** (confirm filename)
Press: **Ctrl+X** (exit editor)

You should be back at the command prompt.

### 8. Verify the Changes

```bash
cat .env | grep -A 10 "AWS_S3"
```

You should see your S3 configuration printed out.

### 9. Restart the Application

```bash
cd /opt/movieweave
docker-compose restart app
```

Wait for it to complete (should take 10-15 seconds).

### 10. Verify Restart Succeeded

```bash
docker-compose logs -f app
```

Watch the logs for 10 seconds. You should see:
- Application starting
- Connecting to database
- Loading configuration
- Server running on port 8000

Press **Ctrl+C** to exit the logs.

---

## ✅ Expected Output Examples

### After saving .env:
```
ubuntu@ip-172-26-xx-xxx:/opt/movieweave$ cat .env | grep -A 10 "AWS_S3"
AWS_S3_BUCKET=movieweave-storage
AWS_REGION=us-east-1
AWS_S3_ENABLED=true
S3_UPLOAD_DIR=videos/uploads
S3_OUTPUT_DIR=videos/output
S3_BACKUP_DIR=backups
```

### After restart:
```
ubuntu@ip-172-26-xx-xxx:/opt/movieweave$ docker-compose restart app
Restarting app ... done
```

### When checking logs:
```
app_1  | Starting FastAPI application...
app_1  | Loaded configuration from .env
app_1  | AWS S3 enabled: True
app_1  | S3 Bucket: movieweave-storage
app_1  | S3 Region: us-east-1
app_1  | Application ready on 0.0.0.0:8000
```

---

## 🎯 What Happened

Your Lightsail instance now knows:
- ✅ S3 bucket name: `movieweave-storage`
- ✅ S3 region: `us-east-1`
- ✅ S3 is enabled
- ✅ Where to upload files: `videos/uploads`
- ✅ Where to store outputs: `videos/output`
- ✅ Where to store backups: `backups`

---

## ✨ Phase 5 Complete!

Once you see the app restart successfully and S3 configuration in logs, Phase 5 is done! ✅

**Next: Phase 6** - Test S3 connection with a Python script.

Reply when done! 🚀
