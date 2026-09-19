# 📋 PHASE 2: Create Lifecycle Policy - QUICK GUIDE

## What This Does

Automatically moves videos to cheaper storage over time:
- **Days 1-30:** Standard storage ($0.023/GB) - Fast
- **Days 30-90:** Standard-IA ($0.0125/GB) - 45% cheaper
- **Days 90-365:** Glacier ($0.004/GB) - 83% cheaper  
- **After 365 days:** Auto-delete

**Savings:** ~$200/year per 1TB! 💰

---

## 🔧 STEP-BY-STEP

### 1. Open AWS S3 Console
Go to: https://console.aws.amazon.com/s3/

### 2. Click Your Bucket
Click: **movieweave-storage**

### 3. Go to Management Tab
Click the **"Management"** tab at the top

### 4. Create Lifecycle Rule
Click **"Create lifecycle rule"** button

---

## 📝 FILL IN THE FORM

**Rule name:**
```
archive-old-videos
```

**Apply to:** ✓ **All objects in the bucket**

**Check these boxes:**
- ✓ Transition current versions of objects between storage classes
- ✓ Expire current versions of objects

---

## 🔄 ADD TRANSITIONS

**First transition:**
- Storage class: **Standard-IA**
- Days: **30**

**Second transition:**
- Storage class: **Glacier Instant Retrieval**
- Days: **90**

---

## ⏰ ADD EXPIRATION

**Expire after:** **365** days

---

## ✅ CREATE

Click **"Create rule"** button

**Expected:** Success message appears ✅

You should see the rule listed as "Enabled" in Lifecycle rules section.

---

## ✨ Phase 2 Complete!

Ready for Phase 3? Reply when done! 🚀
