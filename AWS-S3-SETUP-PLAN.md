# 🚀 MovieWeave S3 Complete Setup & Integration Plan

## ✅ STATUS: You're Ready to Set Up S3!

You have:
- ✅ GitHub repository configured with all workflows
- ✅ GitHub Actions secrets added (SSH key, Lightsail IP, AWS credentials)
- ✅ Lightsail instance running at `34.204.47.202`
- ⏳ **NOW:** Create S3 bucket and configure it

---

## 📋 QUICK SETUP CHECKLIST (45 minutes total)

### Phase 1: Create S3 Bucket (5 min)
Follow: `/docs/AWS-S3-SETUP-GUIDE.md` - STEP 1

**Do this:**
1. Go to https://console.aws.amazon.com/s3/
2. Click "Create bucket"
3. Name: `movieweave-storage`
4. Region: `us-east-1`
5. Block ALL public access ✓
6. Create!

**Result:** Private S3 bucket ✅

---

### Phase 2: Lifecycle Policy (5 min)
Follow: `/docs/AWS-S3-SETUP-GUIDE.md` - STEP 2

**Do this:**
1. Click your bucket → "Management" tab
2. Create lifecycle rule:
   - Day 30 → Standard-IA (45% cheaper)
   - Day 90 → Glacier (83% cheaper)
   - Day 365 → Delete

**Result:** Old videos auto-archive, save money 💰

---

### Phase 3: IAM Policy (5 min)
Follow: `/docs/AWS-S3-SETUP-GUIDE.md` - STEP 3

**Do this:**
1. Go to IAM → Policies
2. Create policy: `MovieWeave-S3-Access-Only`
3. Paste JSON from guide
4. Create!

**Result:** Restricted access policy ✅

---

### Phase 4: Attach to User (3 min)
Follow: `/docs/AWS-S3-SETUP-GUIDE.md` - STEP 4

**Do this:**
1. Go to IAM → Users → Your GitHub user
2. Add permissions → Attach policy
3. Select: `MovieWeave-S3-Access-Only`
4. Attach!

**Result:** User has S3 access ✅

---

### Phase 5: Update Lightsail (10 min)
Follow: `/docs/AWS-S3-SETUP-GUIDE.md` - STEP 5

```bash
ssh -i /path/to/MovieWeave-instance.pem ubuntu@34.204.47.202
cd /opt/movieweave
nano .env
```

**Add these lines:**
```env
AWS_S3_BUCKET=movieweave-storage
AWS_REGION=us-east-1
AWS_S3_ENABLED=true
S3_UPLOAD_DIR=videos/uploads
S3_OUTPUT_DIR=videos/output
S3_BACKUP_DIR=backups
```

**Save:** Ctrl+O, Enter, Ctrl+X

**Restart:**
```bash
docker-compose restart app
```

**Result:** Lightsail knows about S3 ✅

---

### Phase 6: Test Connection (5 min)
Follow: `/docs/AWS-S3-SETUP-GUIDE.md` - STEP 6

```bash
ssh -i /path/to/MovieWeave-instance.pem ubuntu@34.204.47.202
python3 << 'EOF'
import boto3
try:
    s3_client = boto3.client('s3', region_name='us-east-1')
    response = s3_client.list_buckets()


---

## 💰 COST BREAKDOWN

### Monthly S3 Costs (Example: 100GB)

| Component | Cost |
|-----------|------|
| Storage (Standard, month 1) | $2.30 |
| Data transfer OUT | $0-$10 |
| S3 requests | $1.00 |
| **Total/month** | **~$13.30** |

**With Lifecycle Policy (after 90 days):**
- Months 1-1: Standard ($2.30)
- Months 1-3: Standard-IA ($1.25) ← 45% cheaper
- Months 3-12: Glacier ($0.40) ← 83% cheaper
- After 1 year: Deleted ($0)

**Annual: ~$40-50 for 100GB** (vs $280+ without policy)

---

## 🔒 SECURITY CHECKLIST

✅ **DO:**
- Keep bucket private (block all public access)
- Use least-privilege IAM policies
- Monitor bucket access
- Enable versioning for critical videos

❌ **DON'T:**
- Make bucket public
- Use root AWS account
- Share credentials in code/Git
- Upload unlimited data

---

## 🆘 TROUBLESHOOTING

### "Access Denied" Error

**Cause:** AWS credentials or IAM policy issue

**Fix:**
```bash
# 1. Verify credentials in GitHub Secrets are correct
# 2. Confirm IAM policy attached to user
# 3. Check bucket name: movieweave-storage
# 4. Restart app: docker-compose restart app
```

### "NoSuchBucket" Error

**Cause:** Bucket doesn't exist or wrong region

**Fix:**
```bash
# 1. Confirm bucket exists in AWS Console
# 2. Verify region is us-east-1
# 3. Check .env has correct bucket name
```

### S3 Connection Fails

**Check logs:**
```bash
ssh -i /path/to/key.pem ubuntu@34.204.47.202
cd /opt/movieweave
docker-compose logs -f app | grep -i s3
```

---

## ✅ FINAL VERIFICATION

After all phases, verify:

- [ ] S3 bucket exists: `movieweave-storage`
- [ ] Bucket is private (all public access blocked)
- [ ] Lifecycle policy created: `archive-old-videos`
- [ ] IAM policy created: `MovieWeave-S3-Access-Only`
- [ ] Policy attached to GitHub Actions user
- [ ] Lightsail `.env` updated with S3 settings
- [ ] App restarted: `docker-compose restart app`
- [ ] S3 connection test passed
- [ ] Deployment completed successfully
- [ ] API health check passes

**Once all checked: S3 is fully integrated!** 🎉

---

## 🚀 YOU'RE ALL SET!

**Total time:** 45 minutes to complete S3 setup

**Next step:** Follow the checklist in order starting with Phase 1

**Expected result:** 
- ✅ Videos stored in S3
- ✅ Automatic cost savings with lifecycle policy
- ✅ Full GitHub Actions CI/CD pipeline
- ✅ Production-ready MovieWeave application

**Let's get started!** 🎬

    print("✅ S3 Connection successful!")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

**Expected:** `✅ S3 Connection successful!`

**Result:** S3 is connected! 🎉

---

### Phase 7: Deploy (5 min)

```bash
cd /Users/karthiksankaran/MovieWeave
git add .
git commit -m "feat: enable S3 integration"
git push origin main
```

**Watch:** https://github.com/karlondon/MovieWeave/actions

**Result:** Full S3 integration live! 🚀
