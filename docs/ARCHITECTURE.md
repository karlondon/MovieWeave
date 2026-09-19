# MovieWeave System Architecture

## 🏗️ High-Level Overview

MovieWeave is deployed on AWS Lightsail (4GB, 2 vCPU, 80GB SSD) with external S3 storage (256GB).

```
Users → HTTPS (Nginx) → FastAPI Backend → Toonflow Animation
                             ↓                    ↓
                        Local Storage (80GB)  S3 Archive
                             ↓
                        AWS Polly (TTS)
```

## 📊 Component Architecture

### Lightsail Instance (34.204.47.202)
```
┌─ Nginx Reverse Proxy (Ports 80/443)
│   └─ SSL/TLS termination
│   └─ Route to services
│
├─ FastAPI Backend (Port 8000)
│   └─ Document upload
│   └─ Job management
│   └─ S3 integration
│   └─ Polly TTS calls
│   └─ Video orchestration
│
├─ Toonflow (Port 10588)
│   └─ Animation rendering
│   └─ Scene composition
│   └─ Video generation
│
└─ Local Storage (80GB SSD)
    ├─ /data/uploads/   (temporary)
    ├─ /data/output/    (processed)
    ├─ /data/temp/      (working)
    └─ /data/jobs_db.json (tracking)
```

### AWS Services
- **S3 Bucket:** movieweave-storage (256GB)
- **Polly:** Text-to-Speech neural voices
- **Region:** us-east-1 (same as instance)

## 🔄 Data Flow: Video Generation

1. User uploads PDF/DOCX document
2. FastAPI saves to local /data/uploads/
3. Background job extracts text
4. AWS Polly generates audio (MP3)
5. Toonflow renders animation
6. Video composed and encoded (MP4)
7. Final video archived to S3
8. User downloads via secure link

## 💾 Storage Strategy

**Local (Lightsail 80GB):** Temporary files during processing
**S3 (256GB):** Long-term archive of completed videos
**Benefit:** Unlimited scalability + cost-effective

## 🔐 Security

- Firewall: Ports 22, 80, 443, 8000, 10588 only
- SSL/TLS encryption on all traffic
- AWS credentials in .env (not in code)
- S3 bucket: Public access blocked
- SSH: Key-based authentication

## 💰 Cost Structure

| Component | Monthly Cost |
|-----------|-------------|
| Lightsail 4GB/2vCPU | $24 |
| S3 Storage 256GB | $6 |
| S3 Requests | $1 |
| Data Transfer | $8 |
| AWS Polly | $10 |
| **TOTAL** | **~$50** |

## 📈 Scalability

**Current (MVP):** 100-150 videos/month
**Medium:** 500 videos/month (upgrade instance)
**Enterprise:** 2000+ videos/month (add CDN)
