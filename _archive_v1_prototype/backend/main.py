import os
import logging
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict
from threading import Lock

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
from dotenv import load_dotenv
import pdfplumber
import aiofiles

from ffmpeg_video import generate_mp4_ffmpeg

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
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/data/uploads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/data/output"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", "/data/temp"))
JOBS_DB_FILE = Path(os.getenv("JOBS_DB_FILE", "/data/jobs_db.json"))

# Create directories
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ===== AWS CLIENTS =====
s3_client = None
polly_client = None

def init_aws_clients():
    """Initialize AWS clients - checks for credentials at runtime"""
    global s3_client, polly_client
    
    try:
        aws_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        if aws_key and aws_secret:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_key,
                aws_secret_access_key=aws_secret,
                region_name=aws_region
            )
            logger.info("✅ S3 client initialized")
        else:
            logger.warning("⚠️ AWS credentials not configured for S3")
            s3_client = None
    except Exception as e:
        logger.error(f"❌ S3 init failed: {e}")
        s3_client = None
    
    try:
        aws_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        if aws_key and aws_secret:
            polly_client = boto3.client(
                'polly',
                aws_access_key_id=aws_key,
                aws_secret_access_key=aws_secret,
                region_name=aws_region
            )
            logger.info("✅ Polly client initialized")
        else:
            logger.warning("⚠️ AWS credentials not configured for Polly")
            polly_client = None
    except Exception as e:
        logger.error(f"❌ Polly init failed: {e}")
        polly_client = None

# Initialize AWS clients on startup
init_aws_clients()

# ===== DATA MODELS =====
class Health(BaseModel):
    status: str
    version: str
    aws_ok: bool
    s3_ok: bool
    polly_ok: bool


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

# ===== JOBS DATABASE =====
class JobsDB:
    def __init__(self, db_file: Path):
        self.db_file = db_file
        self.lock = Lock()
        if not self.db_file.exists():
            self.db_file.write_text(json.dumps({}))
    
    def get_all(self) -> Dict:
        with self.lock:
            try:
                return json.loads(self.db_file.read_text())
            except:
                return {}
    
    def get(self, job_id: str) -> Dict:
        with self.lock:
            jobs = json.loads(self.db_file.read_text())
            return jobs.get(job_id, {})
    
    def set(self, job_id: str, data: Dict):
        with self.lock:
            jobs = json.loads(self.db_file.read_text())
            jobs[job_id] = data
            self.db_file.write_text(json.dumps(jobs, indent=2))

jobs_db = JobsDB(JOBS_DB_FILE)

# ===== API ENDPOINTS =====

@app.get("/")
async def root():
    """API Root - Returns welcome message"""
    return {
        "message": "Welcome to MovieWeave API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=Health)
async def health():
    """Health check endpoint"""
    return Health(
        status="healthy",
        version="1.0.0",
        aws_ok=s3_client is not None and polly_client is not None,
        s3_ok=s3_client is not None,
        polly_ok=polly_client is not None
    )

@app.post("/upload", response_model=UploadResponse)
async def upload(
    bg: BackgroundTasks,
    file: UploadFile = File(...),
    multi_voice: bool = True
):
    """Upload PDF file and start conversion"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    job_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        jobs_db.set(job_id, {
            "job_id": job_id,
            "status": "processing",
            "progress": 0,
            "filename": file.filename,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })
        
        bg.add_task(process_pdf, job_id, file_path)
        
        return UploadResponse(
            job_id=job_id,
            status="processing",
            message=f"File {file.filename} uploaded successfully. Processing started."
        )
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/job/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get job status"""
    job = jobs_db.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatus(
        job_id=job['job_id'],
        status=job['status'],
        progress=job.get('progress', 0),
        created_at=job['created_at'],
        updated_at=job['updated_at']
    )

@app.get("/jobs")
async def list_jobs():
    """List all jobs"""
    return jobs_db.get_all()

@app.get("/download/{job_id}")
async def download_file(job_id: str, format: str = 'mp4'):
    """Download output file (MP3 or MP4). Query param: ?format=mp3 or ?format=mp4"""
    job = jobs_db.get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Job is not completed")
    
    # Try to find the output file
    job_dir = OUTPUT_DIR / job_id
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Output directory not found")
    
    # Look for requested format (prefer MP4 if available, fallback to MP3)
    output_file = None
    media_type = None
    
    if format.lower() == 'mp4':
        # Try MP4 first
        output_file = job_dir / "output.mp4"
        if output_file.exists():
            media_type = "video/mp4"
        else:
            # Fallback to MP3
            output_file = job_dir / "output.mp3"
            if output_file.exists():
                media_type = "audio/mpeg"
    else:
        # Try MP3 first
        output_file = job_dir / "output.mp3"
        if output_file.exists():
            media_type = "audio/mpeg"
        else:
            # Fallback to MP4
            output_file = job_dir / "output.mp4"
            if output_file.exists():
                media_type = "video/mp4"
    
    # If still not found, get any file
    if not output_file or not output_file.exists():
        output_files = list(job_dir.glob("*"))
        if not output_files:
            raise HTTPException(status_code=404, detail="No output file found")
        output_file = output_files[0]
        media_type = "application/octet-stream"
    
    if not output_file.is_file():
        raise HTTPException(status_code=404, detail="Output is not a file")
    
    logger.info(f"Downloading file: {output_file} (format={format})")
    
    return FileResponse(
        path=output_file,
        media_type=media_type,
        filename=output_file.name
    )

@app.post("/reset")
async def reset_all_data():
    """Reset all jobs and data - for testing/development only"""
    try:
        # Clear jobs database
        jobs_db.clear()
        logger.info("Jobs database cleared")
        
        # Delete all data directories
        import shutil
        for directory in [OUTPUT_DIR, UPLOAD_DIR, TEMP_DIR]:
            if directory.exists():
                shutil.rmtree(directory)
                directory.mkdir(parents=True, exist_ok=True)
        
        logger.info("All data directories reset")
        
        return {"status": "success", "message": "All data has been reset"}
    except Exception as e:
        logger.error(f"Reset failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== BACKGROUND TASKS =====

async def process_pdf(job_id: str, file_path: Path):
    """Process PDF file: extract text, generate audio, create video"""
    try:
        jobs_db.set(job_id, {
            **jobs_db.get(job_id),
            "status": "processing",
            "progress": 25,
            "updated_at": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Extracting text from {file_path}")
        text_content = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text_content += page.extract_text() or ""
                    progress = 25 + int((i / len(pdf.pages)) * 20)
                    jobs_db.set(job_id, {
                        **jobs_db.get(job_id),
                        "progress": progress,
                        "updated_at": datetime.utcnow().isoformat()
                    })
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            raise
        
        # Limit text to first 3000 characters to avoid excessive Polly costs
        text_content = text_content[:3000]
        logger.info(f"Extracted {len(text_content)} characters from PDF")
        
        if s3_client:
            try:
                bucket = os.getenv("AWS_S3_BUCKET", "movieweave-storage")
                s3_key = f"uploads/{job_id}/{file_path.name}"
                s3_client.upload_file(str(file_path), bucket, s3_key)
                logger.info(f"Uploaded {s3_key} to S3")
            except Exception as e:
                logger.error(f"S3 upload failed: {e}")
        
        # Generate audio using AWS Polly
        jobs_db.set(job_id, {
            **jobs_db.get(job_id),
            "progress": 50,
            "updated_at": datetime.utcnow().isoformat()
        })
        
        audio_file = TEMP_DIR / f"{job_id}.mp3"
        if polly_client:
            try:
                logger.info(f"Generating audio for job {job_id}")
                response = polly_client.synthesize_speech(
                    Text=text_content,
                    OutputFormat='mp3',
                    VoiceId='Joanna'  # or another voice
                )
                
                with open(audio_file, 'wb') as f:
                    f.write(response['AudioStream'].read())
                logger.info(f"Audio generated: {audio_file}")
                
            except Exception as e:
                logger.error(f"Polly synthesis failed: {e}")
                audio_file = None
        else:
            logger.warning("Polly client not available, skipping audio generation")
            audio_file = None
        
        # Create output directory
        output_dir = OUTPUT_DIR / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory created: {output_dir}")
        
        # Save MP3 audio file
        if audio_file and audio_file.exists():
            output_mp3 = output_dir / "output.mp3"
            import shutil
            shutil.copy(audio_file, output_mp3)
            logger.info(f"✅ MP3 audio file saved: {output_mp3}")
        else:
            # If no audio (Polly not working), create a simple text transcript
            logger.warning(f"⚠️ Audio file not generated, creating transcript instead")
            output_file = output_dir / "transcript.txt"
            try:
                with open(output_file, 'w') as f:
                    f.write(f"Transcript extracted from: {file_path.name}\n")
                    f.write(f"Generated at: {datetime.utcnow().isoformat()}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(text_content)
                logger.info(f"✅ Transcript file created: {output_file}")
            except Exception as e:
                logger.error(f"❌ Failed to create transcript: {e}")
                raise
        
        # Generate MP4 video with animated character if audio exists
        # Using FFmpeg-based generator (10x faster than MoviePy)
        if audio_file and audio_file.exists():
            jobs_db.set(job_id, {
                **jobs_db.get(job_id),
                "progress": 70,
                "updated_at": datetime.utcnow().isoformat()
            })
            
            output_mp4 = output_dir / "output.mp4"
            
            def video_progress(progress):
                """Callback to update job progress during video generation"""
                jobs_db.set(job_id, {
                    **jobs_db.get(job_id),
                    "progress": 70 + int((progress / 100) * 25),
                    "updated_at": datetime.utcnow().isoformat()
                })
            
            # Choose random character type for variety
            import random
            character_types = ['male', 'female', 'animal']
            chosen_character = random.choice(character_types)
            
            logger.info(f"🎬 Generating MP4 video with {chosen_character} character...")
            success = await generate_mp4_ffmpeg(
                audio_path=audio_file,
                text_content=text_content,
                output_path=output_mp4,
                character_type=chosen_character,
                progress_callback=video_progress
            )
            
            if success and output_mp4.exists():
                logger.info(f"✅ MP4 video generated successfully: {output_mp4}")
            else:
                logger.warning(f"⚠️ MP4 generation failed, but MP3 is available")

        
        jobs_db.set(job_id, {
            **jobs_db.get(job_id),
            "status": "completed",
            "progress": 100,
            "updated_at": datetime.utcnow().isoformat()
        })
        logger.info(f"Job {job_id} completed")
        
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        jobs_db.set(job_id, {
            **jobs_db.get(job_id),
            "status": "failed",
            "error": str(e),
            "updated_at": datetime.utcnow().isoformat()
        })

# ===== STARTUP EVENTS =====

@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    logger.info("🚀 MovieWeave API starting up...")
    init_aws_clients()
    logger.info("✅ MovieWeave API ready")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    logger.info("🛑 MovieWeave API shutting down...")



