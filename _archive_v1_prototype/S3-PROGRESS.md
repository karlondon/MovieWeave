# ✅ S3 Bucket Created - Next Steps

Great! Your S3 bucket `movieweave-storage` is now created.

## 📋 COMPLETION STATUS

- ✅ Phase 1: S3 bucket created (`movieweave-storage`)
- ⏳ Phase 2: Lifecycle policy (DO THIS NEXT)
- ⏳ Phase 3: IAM policy
- ⏳ Phase 4: Attach policy to user
- ⏳ Phase 5: Update Lightsail
- ⏳ Phase 6: Test S3 connection
- ⏳ Phase 7: Deploy

---

## 🔄 PHASE 2: Create Lifecycle Policy (5 minutes)

This will automatically move old videos to cheaper storage and save you money! 💰

### Step 1: Navigate to Lifecycle Settings

1. Go to: https://console.aws.amazon.com/s3/
2. Click on your bucket: **movieweave-storage**
3. Click the **"Management"** tab
4. Click **"Create lifecycle rule"** button

### Step 2: Name Your Rule

**Rule name:**
```
archive-old-videos
```

✓ Check: **"Apply to all objects in the bucket"**

### Step 3: Set Up Transitions (Moving Videos to Cheaper Storage)

Click **"Transition current versions of objects between storage classes"** ✓

**First transition:**
- Storage class: **Standard-IA** (Infrequent Access)
- Days after object creation: **30 days**
- Cost impact: 45% cheaper than Standard

**Second transition:**
- Storage class: **Glacier Instant Retrieval**
- Days after object creation: **90 days**
- Cost impact: 83% cheaper than Standard

### Step 4: Set Up Expiration (Auto-Delete Old Videos)

Click **"Expire current versions of objects"** ✓

- Days after object creation: **365 days** (1 year, then delete)

### Step 5: Create the Rule

Click **"Create rule"** button

**Expected result:**
```
Successfully created lifecycle rule 'archive-old-videos'
```

✅ **Lifecycle policy is now active!**

---

## 💰 Cost Impact Example

For 100GB of videos with this lifecycle policy:

```
Month 1-1:     100GB @ $0.023/GB = $2.30     (Standard)
Month 1-3:     100GB @ $0.0125/GB = $1.25    (Standard-IA) ← 45% cheaper
Month 3-12:    100GB @ $0.004/GB = $0.40     (Glacier)    ← 83% cheaper
After 1 year:  Deleted = $0                   (Auto-cleaned)

Annual cost: ~$40-50  (vs $280+ without lifecycle)
Savings: ~$200+ per year! 🎉
```

---

## ✅ Next: Phase 3 - Create IAM Policy

Once the lifecycle policy is created and you see the success message, you're ready for Phase 3!

**Continue with:** `docs/AWS-S3-SETUP-GUIDE.md` - STEP 3

Or run the next command when ready:
```bash
echo "Ready for Phase 3: Create IAM Policy"
```

---

## 🎯 Quick Checklist

- ✅ S3 bucket created: movieweave-storage
- [ ] Lifecycle policy created: archive-old-videos
  - [ ] 30-day transition to Standard-IA
  - [ ] 90-day transition to Glacier
  - [ ] 365-day expiration (delete)

Once lifecycle policy shows "Successfully created", move to Phase 3! ✨
