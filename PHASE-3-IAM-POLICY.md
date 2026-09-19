# 📋 PHASE 3: Create IAM Policy - QUICK GUIDE

## What This Does

Creates a **restricted security policy** that allows your GitHub Actions user to:
- ✅ Upload files to S3
- ✅ Download files from S3
- ✅ Delete files from S3
- ❌ Access anything else in AWS (security best practice)

---

## 🔧 STEP-BY-STEP

### 1. Open AWS IAM Console
Go to: https://console.aws.amazon.com/iam/

### 2. Click "Policies"
In the left sidebar, click: **Policies**

### 3. Create New Policy
Click **"Create policy"** button

### 4. Switch to JSON Tab
You'll see a visual editor. Click the **"JSON"** tab at the top.

### 5. Replace the Code
Delete everything in the text box and paste this:

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

### 6. Click "Next"
Click the **"Next"** button at the bottom right.

### 7. Name the Policy
**Policy name:**
```
MovieWeave-S3-Access-Only
```

**Description (optional):**
```
Allows GitHub Actions to upload/download videos from movieweave-storage S3 bucket only
```

### 8. Create Policy
Click **"Create policy"** button

---

## ✅ Expected Result

You should see a success message:
```
✅ Policy MovieWeave-S3-Access-Only has been created
```

The policy is now created and ready to attach to your user.

---

## 🎯 What This Policy Does

| Action | Allowed |
|--------|---------|
| Upload files to S3 | ✅ Yes |
| Download files from S3 | ✅ Yes |
| Delete files from S3 | ✅ Yes |
| List files in bucket | ✅ Yes |
| Access other AWS services | ❌ No |
| Delete S3 bucket | ❌ No |
| Access other buckets | ❌ No |

This is called **"Least Privilege"** - only the minimum permissions needed.

---

## ✨ Phase 3 Complete!

Once you see the success message, Phase 3 is done! ✅

**Next: Phase 4** - Attach this policy to your GitHub Actions IAM user.

Reply when done! 🚀
