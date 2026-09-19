# 🎬 MovieWeave - START HERE!

## ✅ COMPLETION STATUS: 95% COMPLETE

All GitHub Actions workflows are **live and ready**. You just need to add 2 GitHub Secrets!

---

## 📊 WHAT'S BEEN COMPLETED

### ✅ GitHub Repository Setup
- **Repository:** https://github.com/karlondon/MovieWeave
- **Status:** ✅ Live with SSH access
- **All code:** Pushed successfully
- **Branch:** `main` (production)

### ✅ GitHub Actions Workflows (3 created)

| Workflow | Purpose | Status |
|----------|---------|--------|
| **Deploy** | Auto-deploy on every push to main | ⏳ Needs secrets |
| **Quality Checks** | Lint, test, security scan | ✅ Ready now |
| **Health Check** | Monitor API every 6 hours | ⏳ Needs secrets |

### ✅ Documentation Created
- `GITHUB-ACTIONS-COMPLETE.md` - Complete setup guide
- `DEPLOYMENT-GUIDE.md` - Step-by-step walkthrough
- `GITHUB-SECRETS-SETUP.md` - Secret configuration
- `GITHUB-ACTIONS-SETUP.md` - Workflow details

---

## 🔐 WHAT YOU NEED TO DO NOW (2 Secrets - 5 minutes)

### **Secret #1: LIGHTSAIL_SSH_KEY** ⚠️ CRITICAL

Get your SSH key:
```bash
cat /Users/karthiksankaran/MovieWeave/pem-key/MovieWeave-instance.pem
```

Add to GitHub:
1. Go to: https://github.com/karlondon/MovieWeave/settings/secrets/actions
2. Click **"New repository secret"**
3. **Name:** `LIGHTSAIL_SSH_KEY`
4. **Value:** Paste entire key (BEGIN to END lines)
5. Click **"Add secret"**

---

### **Secret #2: LIGHTSAIL_INSTANCE_IP** ⚠️ CRITICAL

Add to GitHub:
1. Click **"New repository secret"**
2. **Name:** `LIGHTSAIL_INSTANCE_IP`
3. **Value:** `34.204.47.202`
4. Click **"Add secret"**

---

## 🚀 NEXT STEPS (After Adding Secrets)

### **Step 1: Prepare Lightsail Instance (10 minutes)**

```bash
# Connect to Lightsail
ssh -i /path/to/MovieWeave-instance.pem ubuntu@34.204.47.202

# Create deployment directory
sudo mkdir -p /opt/movieweave
sudo chown ubuntu:ubuntu /opt/movieweave
cd /opt/movieweave

# Clone repository
git clone https://github.com/karlondon/MovieWeave.git .

# Create data directories
mkdir -p data/uploads data/output data/temp

# Set up environment
cp .env.example .env
nano .env  # Edit with your AWS credentials
```

**Key .env settings:**
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
APP_ENV=production
DEBUG=false
ALLOWED_HOSTS=34.204.47.202,movieweave.example.com
```

---

### **Step 2: Test Deployment (2 minutes)**

```bash
cd /Users/karthiksankaran/MovieWeave
git add .
git commit -m "test: trigger GitHub Actions"
git push origin main
```

Watch at: https://github.com/karlondon/MovieWeave/actions

---

### **Step 3: Verify Success (1 minute)**

```bash
curl http://34.204.47.202:8000/health
```

Expected: `{"status": "ok"}`

---

## 📋 QUICK CHECKLIST

- [ ] Add `LIGHTSAIL_SSH_KEY` secret
- [ ] Add `LIGHTSAIL_INSTANCE_IP` secret
- [ ] SSH into Lightsail and set up `/opt/movieweave`
- [ ] Create `.env` file on Lightsail
- [ ] Test deployment with `git push origin main`
- [ ] Verify API health check passes

**Then you're done! Every future push = automatic deployment!** 🚀

---

## 🔗 KEY LINKS

| Link | Purpose |
|------|---------|
| https://github.com/karlondon/MovieWeave/settings/secrets/actions | **ADD SECRETS HERE** |
| https://github.com/karlondon/MovieWeave/actions | Watch workflows run |
| http://34.204.47.202:8000/health | Test API health |
| http://34.204.47.202:8000/docs | Swagger API docs |

---

## 📚 DETAILED GUIDES

For more detailed information, see:
- `GITHUB-ACTIONS-COMPLETE.md` - Full setup guide
- `DEPLOYMENT-GUIDE.md` - Step-by-step walkthrough
- `GITHUB-SECRETS-SETUP.md` - Secret configuration details
- `docs/GITHUB-ACTIONS-SETUP.md` - Workflow explanations

**You're ready to deploy!** 🎬✨

