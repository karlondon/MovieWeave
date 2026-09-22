# MovieWeave Deployment Guide

## 📋 Prerequisites

- AWS Account with Lightsail instance created
- Instance IP: 34.204.47.202
- SSH key: `/PS-Scripts/MovieWeave/pem-key/movieweave.pem`
- AWS S3 bucket created: `movieweave-storage`
- AWS Polly enabled in your region

## 🚀 Step 1: Connect to Your Instance

```bash
# Set permissions on SSH key
chmod 600 /Users/karthiksankaran/PS-Scripts/MovieWeave/pem-key/movieweave.pem

# SSH into the instance
ssh -i /Users/karthiksankaran/PS-Scripts/MovieWeave/pem-key/movieweave.pem ubuntu@34.204.47.202
```

## 🔧 Step 2: Run Initial Setup

On the instance:

```bash
# Clone or download your MovieWeave files to /opt/movieweave
cd /opt/movieweave

# Make setup script executable
chmod +x scripts/initial-setup.sh

# Run initial setup (requires sudo)
sudo bash scripts/initial-setup.sh
```

This script will:
- ✅ Update system packages
- ✅ Install Docker & Docker Compose
- ✅ Install Python 3.11, FFmpeg, Nginx
- ✅ Install Node.js for Toonflow
- ✅ Create application directories
- ✅ Configure firewall (open ports 22, 80, 443, 8000, 10588)
- ✅ Create 4GB swap file
- ✅ Create `.env` file

## 🔐 Step 3: Configure Environment Variables

After setup, edit the `.env` file:

```bash
nano .env
```

Fill in your AWS credentials:

```env
AWS_ACCESS_KEY_ID=your_actual_aws_key
AWS_SECRET_ACCESS_KEY=your_actual_aws_secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=movieweave-storage
AWS_POLLY_REGION=us-east-1
```

Save and exit (Ctrl+X, then Y, then Enter).

## 🐳 Step 4: Deploy Application

```bash
cd /opt/movieweave

# Make deploy script executable
chmod +x scripts/deploy.sh

# Run deployment
bash scripts/deploy.sh
```

This will:
- ✅ Build Docker images
- ✅ Start FastAPI backend
- ✅ Start Toonflow service
- ✅ Start Nginx reverse proxy

## ✅ Step 5: Verify Deployment

```bash
# Check if services are running
docker-compose ps

# View logs
docker-compose logs -f

# Health check
curl http://localhost:8000/health

# API Swagger documentation
# Open in browser: http://34.204.47.202:8000/docs
```

## 🔒 Step 6: Setup SSL Certificate (HTTPS)

```bash
# Install certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --standalone -d movieweave.myblognow.uk

# Update Nginx config with certificate paths
sudo systemctl restart nginx
```

## 📊 Step 7: Verify Everything Works

1. **Health Check**
   ```bash
   curl https://movieweave.myblognow.uk/health
   ```

2. **API Docs**
   - Visit: `https://movieweave.myblognow.uk/docs`

3. **Upload a Test File**
   ```bash
   curl -X POST "https://movieweave.myblognow.uk/api/upload" \
     -F "file=@test.pdf"
   ```

## 🛠️ Troubleshooting

### Check Logs
```bash
# FastAPI logs
docker-compose logs movieweave-api

# Nginx logs
docker-compose logs nginx

# Toonflow logs
docker-compose logs toonflow
```

### Restart Services
```bash
# Stop all services
docker-compose down

# Start again
docker-compose up -d
```

### S3 Connection Issues
- Verify AWS credentials in `.env`
- Check S3 bucket exists and is accessible
- Ensure IAM user has S3 permissions

### Port Already in Use
```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill process if needed
sudo kill -9 <PID>
```

## 📈 Monitoring

### View Real-time Logs
```bash
docker-compose logs -f --tail=100
```

### Check Disk Usage
```bash
df -h
du -sh /opt/movieweave/data/
```

### Monitor S3 Uploads
```bash
aws s3 ls movieweave-storage/ --recursive --summarize
```

## 🔄 Updating Application

To deploy new code changes:

```bash
# Pull latest changes
cd /opt/movieweave
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

## 💾 Backup

Create a backup of jobs database:

```bash
# Backup jobs
cp /opt/movieweave/data/jobs_db.json /opt/movieweave/backups/jobs_$(date +%Y%m%d).json

# Upload to S3
aws s3 cp /opt/movieweave/backups/ s3://movieweave-storage/backups/ --recursive
```

## 📞 Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Verify AWS credentials
3. Check disk space: `df -h`
4. Check memory: `free -h`
5. Restart services: `docker-compose restart`

## ✨ Next Steps

- [ ] Configure domain DNS to point to instance IP
- [ ] Setup automated backups to S3
- [ ] Configure CloudWatch monitoring
- [ ] Setup auto-scaling policies
- [ ] Launch marketing campaign
- [ ] Monitor costs in AWS console
