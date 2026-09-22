"""
worker.py - Background job processor worker
Runs independently and continuously processes pending jobs
"""
import asyncio
import logging
import time
from pathlib import Path

from app.config import settings
from app.utils.logger import setup_logging
from app.utils.job_manager import JobManager
from app.utils.processor import process_job

# Setup logging
logger = setup_logging(settings.LOGS_DIR, app_name="sceneweave-worker")

job_manager = JobManager()

async def process_pending_jobs():
    """Continuously poll for pending jobs and process them"""
    logger.info("=" * 80)
    logger.info("🚀 Starting SceneWeave Job Worker")
    logger.info("=" * 80)
    
    while True:
        try:
            # Reload jobs from disk to get latest updates from API
            job_manager.jobs = job_manager._load_jobs()
            
            # Get all pending jobs
            all_jobs = job_manager.list_all_jobs()
            pending_jobs = [j for j in all_jobs if j["status"] == "pending"]
            
            if pending_jobs:
                logger.info(f"📋 Found {len(pending_jobs)} pending job(s)")
                
                for job in pending_jobs:
                    job_id = job["job_id"]
                    file_path = job["file_path"]
                    
                    # Check if file exists
                    if not Path(file_path).exists():
                        logger.error(f"❌ File not found for job {job_id}: {file_path}")
                        job_manager.update_job(
                            job_id,
                            status="failed",
                            message="File not found",
                            error="Upload file missing"
                        )
                        continue
                    
                    logger.info(f"🎬 Processing job: {job_id}")
                    try:
                        # Process the job (this is async)
                        await process_job(job_id, file_path)
                        logger.info(f"✅ Completed job: {job_id}")
                    except Exception as e:
                        logger.error(f"❌ Failed job {job_id}: {e}", exc_info=True)
                        job_manager.update_job(
                            job_id,
                            status="failed",
                            message="Processing error",
                            error=str(e)
                        )
            else:
                logger.debug("⏳ No pending jobs, waiting...")
            
            # Check every 5 seconds for new jobs
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"❌ Worker error: {e}", exc_info=True)
            await asyncio.sleep(10)  # Wait longer on error

async def main():
    """Main worker entry point"""
    try:
        await process_pending_jobs()
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down worker")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
