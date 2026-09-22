# 📋 PHASE 4: Attach Policy to IAM User - QUICK GUIDE

## What This Does

Connects the `MovieWeave-S3-Access-Only` policy to your GitHub Actions IAM user so they can access S3.

---

## 🔧 STEP-BY-STEP

### 1. Go to IAM Users
Go to: https://console.aws.amazon.com/iam/home#/users

You'll see a list of all your IAM users.

### 2. Find Your GitHub Actions User

Look for a user named something like:
- `movieweave-github-actions`
- `github-actions`
- `movieweave-user`
- Or whatever you named your GitHub Actions IAM user

**Click on the username** to open their details.

### 3. Go to Permissions Tab

You'll see several tabs at the top. Click: **"Permissions"** tab

### 4. Add Permissions

Click the **"Add permissions"** button (top right)

A dropdown menu will appear. Click: **"Attach policies directly"**

### 5. Search for Your Policy

In the search box, type:
```
MovieWeave-S3-Access-Only
```

You should see the policy appear in the search results.

### 6. Select the Policy

**Click the checkbox** ✓ next to `MovieWeave-S3-Access-Only`

### 7. Attach Policy

Click the **"Add permissions"** button at the bottom right.

---

## ✅ Expected Result

You'll see a success message and the policy will appear in the user's permission list:

```
MovieWeave-S3-Access-Only          Customer managed          Attached
```

---

## 🎯 What Happened

Your GitHub Actions user now has:
- ✅ Access to upload files to S3
- ✅ Access to download files from S3
- ✅ Access to delete files from S3
- ❌ Access to anything else in AWS
- ❌ Permission to delete the bucket or create new buckets

This is the safest way to integrate AWS with GitHub Actions!

---

## ✨ Phase 4 Complete!

Once you see the policy attached to your user, Phase 4 is done! ✅

**Next: Phase 5** - Update your Lightsail instance with S3 configuration.

Reply when done! 🚀
