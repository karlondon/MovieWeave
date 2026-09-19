import os
import logging
import json
import uuid
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
from dotenv import load_dotenv
import pdfplumber
import aiofiles

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MovieWeave",
    description="Convert novels into animated videos",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== CONFIGURATION =====
FREE_CONVERSIONS_PER_DAY = int(os.getenv("FREE_CONVERSIONS_PER_DAY", 3))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "data/uploads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "data/output"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", "data/temp"))
JOBS_DB_FILE = Path(os.getenv("JOBS_DB_FILE", "data/jobs_db.json"))

# Create directories
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ===== AWS CLIENTS =====
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    logger.info("✅ S3 client initialized")
except Exception as e:
    logger.error(f"❌ S3 init failed: {e}")
    s3_client = None

try:
    polly_client = boto3.client(
        'polly',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_POLLY_REGION', 'us-east-1')
    )
    logger.info("✅ Polly client initialized")
except Exception as e:
    logger.error(f"❌ Polly init failed: {e}")
    polly_client = None

# ===== DATA MODELS =====
class Health(BaseModel):
    status: str
    version: str
    aws_ok: bool

class UploadResponse(BaseModel):
    job_id: str
    status: str
    message: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    created_at: str
    updated_at: str
