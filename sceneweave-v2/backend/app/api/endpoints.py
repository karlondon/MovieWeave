"""
endpoints.py - FastAPI routes for SceneWeave MVP (Phases 1-4)
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from datetime import datetime
import logging
from pathlib import Path

from app.config import settings
from app.schemas import UploadResponse, JobStatusResponse, HealthResponse, JobStatus
from app.utils.file_handler import FileHandler
from app.utils.job_manager import JobManager
from app.utils.errors import FileUploadError, InvalidFileTypeError, FileSizeError
from app.utils.llm_processor import GroqScriptGenerator, create_generator
from app.utils.tts_engine import KokoroTTSEngine
from app.utils.video_composer import FFmpegVideoComposer

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["api"])

# Global instances
job_manager = JobManager()
script_generator = None  # Lazy init - will be initialized on first use
tts_engine = KokoroTTSEngine(settings.OUTPUT_DIR)
video_composer = FFmpegVideoComposer(settings.OUTPUT_DIR, settings.TEMP_DIR)

def get_script_generator():
    """Get or create script generator (lazy initialization)"""
    global script_generator
    if script_generator is None:
        script_generator = create_generator()
    return script_generator

# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """API health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow()
    )

# ============================================================================
# FILE UPLOAD (Phase 1)
# ============================================================================

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Upload text file for video generation"""
    try:
        logger.info(f"📤 Upload: {file.filename}")
        content = await file.read()
        
        FileHandler.validate_file(file.filename, len(content))
        job_id, file_path = FileHandler.save_uploaded_file(content, file.filename)
        job_manager.create_job(job_id, file.filename, str(file_path))
        
        if background_tasks:
            from app.utils.processor import process_job
            background_tasks.add_task(process_job, job_id, str(file_path))
        
        logger.info(f"✅ Upload OK: Job {job_id}")
        
        return UploadResponse(
            job_id=job_id,
            filename=file.filename,
            status=JobStatus.PENDING,
            message="Processing started",
            timestamp=datetime.utcnow()
        )
        
    except FileSizeError as e:
        raise HTTPException(status_code=413, detail=e.message)
    except InvalidFileTypeError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except FileUploadError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Upload failed")

# ============================================================================
# JOB STATUS
# ============================================================================

@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get job status and progress"""
    try:
        job = job_manager.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
        return JobStatusResponse(
            job_id=job["job_id"],
            filename=job["filename"],
            status=job["status"],
            progress=job.get("progress", 0),
            message=job.get("message"),
            error=job.get("error"),
            output_file=job.get("output_file"),
            created_at=job["created_at"],
            updated_at=job["updated_at"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed")

@router.get("/jobs")
async def list_jobs():
    """List all jobs"""
    try:
        return job_manager.list_all_jobs()
    except Exception as e:
        logger.error(f"List error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list")

@router.get("/download/{job_id}")
async def download_output(job_id: str):
    """Download generated video"""
    try:
        job = job_manager.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        output_file = job.get("output_file")
        if not output_file or not Path(output_file).exists():
            raise HTTPException(status_code=404, detail="Output not ready")
        
        return FileResponse(output_file, media_type="video/mp4", filename=f"{job_id}.mp4")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Download failed")
