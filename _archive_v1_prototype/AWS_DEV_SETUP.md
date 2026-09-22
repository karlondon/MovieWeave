# AWS Infrastructure Setup for V2.0 Development

## Overview
Create a dedicated EC2 development instance (separate from production V1.0)

**Setup:**
```
Production (V1.0.0)     →  EC2 t3.medium (main branch)
Development (V2.0.0)    →  EC2 t3.medium (feature branches)
```

---

## AWS Resources Needed

### EC2 Instance
- **Type:** t3.medium (2 vCPU, 4GB RAM)
- **OS:** Ubuntu 22.04 LTS
- **Storage:** 50GB gp3 EBS
- **Name:** movieweave-dev-v2

### Security Group
- SSH (port 22) from your IP
- HTTP (port 80) from anywhere
- HTTPS (port 443) from anywhere

### IAM Role
- S3 read/write (for assets/videos)
- Polly access (TTS)
- CloudWatch logs
- ECR access

---

## Quick AWS CLI Commands

```bash
# 1. Get your VPC ID
aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query 'Vpcs[0].VpcId'

# 2. Create security group
SG_ID=$(aws ec2 create-security-group \
  --group-name movieweave-dev-sg \
  --description "MovieWeave V2.0 Dev" \
  --vpc-id vpc-xxxxx \
  --query 'GroupId' --output text)

# 3. Add firewall rules
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr YOUR.IP.ADDRESS/32
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 443 --cidr 0.0.0.0/0

# 4. Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name YOUR_KEY_PAIR \
  --security-group-ids $SG_ID \
  --block-device-mappings DeviceName=/dev/sda1,Ebs={VolumeSize=50,VolumeType=gp3} \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=movieweave-dev-v2}]'

# 5. Get public IP
aws ec2 describe-instances --filters "Name=tag:Name,Values=movieweave-dev-v2" --query 'Reservations[0].Instances[0].PublicIpAddress'

# 6. SSH into instance
ssh -i YOUR_KEY.pem ubuntu@PUBLIC_IP
```

---

## Setup on Instance

```bash
# Install dependencies
sudo apt update && sudo apt install -y docker.io docker-compose git python3-pip rhubarb-lip-sync

# Clone repo
git clone https://github.com/karlondon/MovieWeave.git
cd MovieWeave
git checkout develop

# Build Docker
docker-compose build
docker-compose up -d
```

---

## Cost: ~$40-45/month
- EC2: $30/month
- Storage: $5/month
- Data transfer: $5-10/month

**Save 50% by stopping instance when not developing**
