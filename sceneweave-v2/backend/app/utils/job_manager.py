"""
job_manager.py - Job tracking and management system
"""
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from threading import Lock
import logging

from app.config import settings
from app.schemas import JobStatus

logger = logging.getLogger(__name__)

class JobManager:
    """Manage job lifecycle and state"""
    
    def __init__(self, db_file: Optional[Path] = None):
        """
        Initialize job manager
        
        Args:
            db_file: Path to JSON database file for persistence
        """
        self.db_file = db_file or (settings.TEMP_DIR / "jobs_db.json")
        self.jobs: Dict = self._load_jobs()
        self.lock = Lock()
    
    def _load_jobs(self) -> Dict:
        """Load jobs from persistent storage"""
        try:
            if self.db_file.exists():
                with open(self.db_file, 'r') as f:
                    jobs = json.load(f)
                logger.info(f"✅ Loaded {len(jobs)} jobs from database")
                return jobs
        except Exception as e:
            logger.warning(f"⚠️  Failed to load jobs database: {str(e)}")
        
        return {}
    
    def _save_jobs(self) -> None:
        """Persist jobs to storage"""
        try:
            with open(self.db_file, 'w') as f:
                json.dump(self.jobs, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"❌ Failed to save jobs database: {str(e)}")
    
    def create_job(self, job_id: str, filename: str, file_path: str) -> Dict:
        """
        Create a new job
        
        Args:
            job_id: Unique job identifier
            filename: Original filename
            file_path: Path to uploaded file
            
        Returns:
            Job data dictionary
        """
        with self.lock:
            job = {
                "job_id": job_id,
                "filename": filename,
                "file_path": file_path,
                "status": JobStatus.PENDING,
                "progress": 0,
                "message": "Job created, waiting to process",
                "error": None,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "script_data": None,
                "audio_path": None,
                "video_path": None
            }
            
            self.jobs[job_id] = job
            self._save_jobs()
            logger.info(f"✅ Created job: {job_id} for file: {filename}")
            return job
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """
        Get job by ID
        
        Args:
            job_id: Job identifier
            
        Returns:
            Job data dictionary or None if not found
        """
        # Reload from disk to ensure we have latest data
        self.jobs = self._load_jobs()
        return self.jobs.get(job_id)
    
    def update_job(self, job_id: str, **kwargs) -> Dict:
        """
        Update job status
        
        Args:
            job_id: Job identifier
            **kwargs: Fields to update (status, progress, message, etc.)
            
        Returns:
            Updated job data dictionary
        """
        with self.lock:
            # Reload from disk to ensure we have latest data
            self.jobs = self._load_jobs()
            
            if job_id not in self.jobs:
                raise ValueError(f"Job {job_id} not found")
            
            job = self.jobs[job_id]
            job.update(kwargs)
            job["updated_at"] = datetime.utcnow().isoformat()
            self._save_jobs()
            
            logger.info(f"✅ Updated job {job_id}: {kwargs}")
            return job
    
    def set_processing(self, job_id: str, message: str = "Processing...") -> Dict:
        """Mark job as processing"""
        return self.update_job(
            job_id,
            status=JobStatus.PROCESSING,
            progress=10,
            message=message
        )
    
    def set_completed(self, job_id: str, message: str = "Completed", **extra_data) -> Dict:
        """Mark job as completed"""
        return self.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            progress=100,
            message=message,
            error=None,
            **extra_data
        )
    
    def set_failed(self, job_id: str, error_message: str) -> Dict:
        """Mark job as failed"""
        return self.update_job(
            job_id,
            status=JobStatus.FAILED,
            message="Job failed",
            error=error_message
        )
    
    def list_all_jobs(self) -> list:
        """Get all jobs"""
        # Reload from disk to ensure we have latest data
        self.jobs = self._load_jobs()
        jobs_list = list(self.jobs.values())
        # Sort by creation date (newest first)
        jobs_list.sort(key=lambda x: x["created_at"], reverse=True)
        return jobs_list
    
    def delete_job(self, job_id: str) -> bool:
        """
        Delete a job (cleanup)
        
        Args:
            job_id: Job identifier
            
        Returns:
            True if deleted, False if not found
        """
        with self.lock:
            if job_id in self.jobs:
                del self.jobs[job_id]
                self._save_jobs()
                logger.info(f"🗑️  Deleted job: {job_id}")
                return True
            return False
