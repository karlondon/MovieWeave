# MovieWeave 🎬
## Text-to-Animated Video Platform

Convert novels, long-form documents, and stories into engaging animated videos with character-specific voices and professional narration.

### Instance Details
- **Instance Name**: MovieWeave-instance
- **Instance IP**: 34.204.47.202
- **Specs**: 4GB RAM, 2 vCPU, 80GB SSD
- **Storage**: 256GB S3 bucket attached
- **Region**: us-east-1a
- **SSH Key Location**: `/PS-Scripts/MovieWeave/pem-key/`

### Technology Stack
- **Backend**: FastAPI (Python 3.11)
- **Animation Engine**: Toonflow (Docker)
- **TTS**: AWS Polly (Neural Voices)
- **Video Processing**: FFmpeg
- **Storage**: AWS S3 (External)
- **Payments**: Square SDK
- **Deployment**: Docker + Docker Compose

### Monthly Costs (USD)
| Component | Cost |
|-----------|------|
| Lightsail (4GB) | $24 |
| S3 Storage (256GB) | $5.90 |
| S3 Requests | $1.00 |
| Data Transfer | $8.50 |
| AWS Polly | $10 |
| **TOTAL** | **$49.40/month** |

### Quick Start
1. SSH to instance: `ssh -i pem-key/movieweave.pem ubuntu@34.204.47.202`
2. Run setup: `bash scripts/initial-setup.sh`
3. Deploy: `bash scripts/deploy.sh`
4. Access: `https://movieweave.myblognow.uk`

### Project Structure
```
MovieWeave/
├── pem-key/              # SSH keys
├── backend/              # FastAPI application
│   ├── main.py
│   ├── requirements.txt
│   └── modules/
├── frontend/             # Web UI
│   ├── index.html
│   └── static/
├── docker/               # Docker configs
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/              # Deployment scripts
│   ├── initial-setup.sh
│   ├── deploy.sh
│   └── health-check.sh
├── config/               # Configuration files
│   ├── nginx.conf
│   ├── .env.example
│   └── systemd-movieweave.service
└── docs/                 # Documentation
    ├── DEPLOYMENT.md
    ├── API.md
    └── ARCHITECTURE.md
```

### Next Steps
- [ ] Add SSH key to `pem-key/movieweave.pem`
- [ ] Configure `.env` file with AWS credentials
- [ ] Run initial setup script
- [ ] Deploy application
- [ ] Configure domain: movieweave.myblognow.uk
- [ ] Launch MVP

### Documentation
See detailed documentation in `/docs` folder:
- `DEPLOYMENT.md` - Complete deployment guide
- `API.md` - API endpoint reference
- `ARCHITECTURE.md` - System architecture overview
