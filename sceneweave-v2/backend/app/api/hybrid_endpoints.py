"""
hybrid_endpoints.py - API routes for hybrid curation + auto-generation workflow
Enables curators to manually review stories, then batch process them into videos
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

from app.config import settings
from app.utils.job_manager import JobManager
from app.utils.tts_engine import KokoroTTSEngine
from app.utils.video_composer import FFmpegVideoComposer
from app.utils.lean_processor import LeanVideoProcessor
from app.utils.hybrid_workflow import HybridWorkflowManager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/hybrid", tags=["hybrid-workflow"])

# Global instances
job_manager = JobManager()
tts_engine = KokoroTTSEngine(settings.OUTPUT_DIR)
video_composer = FFmpegVideoComposer(settings.OUTPUT_DIR, settings.TEMP_DIR)
lean_processor = LeanVideoProcessor(job_manager, tts_engine, video_composer)
workflow_manager = HybridWorkflowManager(job_manager, lean_processor)


# ============================================================================
# SCHEMAS
# ============================================================================


class SubmitStoryRequest(BaseModel):
    """Submit story for curator review"""
    title: str
    story_text: str
    source: str = "manual"
    tags: Optional[List[str]] = None


class ReviewStoryRequest(BaseModel):
    """Curator review of story"""
    approved: bool
    notes: Optional[str] = None


class EditStoryRequest(BaseModel):
    """Curator edits story"""
    title: Optional[str] = None
    story_text: Optional[str] = None
    tags: Optional[List[str]] = None


class CreateBatchRequest(BaseModel):
    """Create batch for processing"""
    batch_name: str
    story_ids: Optional[List[str]] = None


# ============================================================================
# CURATOR WORKFLOW ENDPOINTS
# ============================================================================


@router.post("/submit-story")
async def submit_story(request: SubmitStoryRequest):
    """Curator submits story for review"""
    try:
        logger.info(f"📝 Story submission: {request.title}")
        story_id = workflow_manager.submit_story_for_review(
            story_text=request.story_text,
            title=request.title,
            source=request.source,
            tags=request.tags,
        )
        return {
            "success": True,
            "story_id": story_id,
            "status": "pending_review",
            "message": f"Story submitted: {story_id}",
        }
    except Exception as e:
        logger.error(f"❌ Submission failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pending-stories")
async def get_pending_stories():
    """Get all stories awaiting curator review"""
    try:
        pending = workflow_manager.list_pending_stories()
        return {
            "total": len(pending),
            "stories": [
                {
                    "id": s["id"],
                    "title": s["title"],
                    "length": s["length"],
                    "submitted_at": s["submitted_at"],
                }
                for s in pending
            ],
        }
    except Exception as e:
        logger.error(f"Error fetching pending: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review-story/{story_id}")
async def review_story(story_id: str, request: ReviewStoryRequest):
    """Curator approves or rejects story"""
    try:
        success = workflow_manager.review_story(
            story_id=story_id, approved=request.approved, notes=request.notes
        )
        if not success:
            raise HTTPException(status_code=404, detail="Story not found")
        return {
            "success": True,
            "story_id": story_id,
            "status": "approved" if request.approved else "rejected",
        }
    except Exception as e:
        logger.error(f"❌ Review failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/edit-story/{story_id}")
async def edit_story(story_id: str, request: EditStoryRequest):
    """Curator edits story before processing"""
    try:
        updates = {}
        if request.title:
            updates["title"] = request.title
        if request.story_text:
            updates["text"] = request.story_text
        if request.tags:
            updates["tags"] = request.tags
        success = workflow_manager.edit_story(story_id, updates)
        if not success:
            raise HTTPException(status_code=404, detail="Story not found")
        return {
            "success": True,
            "story_id": story_id,
            "message": "Story updated successfully"
        }
    except Exception as e:
        logger.error(f"❌ Edit failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BATCH PROCESSING ENDPOINTS
# ============================================================================


@router.post("/create-batch")
async def create_batch(request: CreateBatchRequest):
    """Create batch of approved stories for processing"""
    try:
        logger.info(f"📦 Creating batch: {request.batch_name}")
        batch_id = workflow_manager.create_processing_batch(
            batch_name=request.batch_name, story_ids=request.story_ids
        )
        if not batch_id:
            raise HTTPException(status_code=400, detail="No approved stories")
        return {
            "success": True,
            "batch_id": batch_id,
            "batch_name": request.batch_name,
        }
    except Exception as e:
        logger.error(f"❌ Batch creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-batch/{batch_id}")
async def process_batch(batch_id: str, background_tasks: BackgroundTasks):
    """Start processing batch in background"""
    try:
        logger.info(f"🎬 Processing batch: {batch_id}")
        result = workflow_manager.process_batch_async(batch_id, background_tasks)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"❌ Batch processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/batch-status/{batch_id}")
async def get_batch_status(batch_id: str):
    """Get batch processing status and results"""
    try:
        batch = workflow_manager._find_batch(batch_id)
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")
        return {
            "batch_id": batch_id,
            "name": batch["name"],
            "status": batch["status"],
            "total_stories": batch["total_stories"],
            "created_at": batch["created_at"],
            "results": batch.get("results", {}),
        }
    except Exception as e:
        logger.error(f"Error getting batch status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# WORKFLOW STATISTICS & EXPORT
# ============================================================================


@router.get("/stats")
async def get_workflow_stats():
    """Get workflow statistics (stories, batches, videos generated)"""
    try:
        stats = workflow_manager.get_stats()
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "stats": stats,
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export-batch/{batch_id}")
async def export_batch_videos(batch_id: str):
    """Export all videos from batch"""
    try:
        exported = workflow_manager.export_batch_videos(batch_id)
        if not exported:
            raise HTTPException(status_code=404, detail="Batch not found")
        return {
            "success": True,
            "batch_id": batch_id,
            "exported_count": len(exported),
            "videos": exported,
        }
    except Exception as e:
        logger.error(f"Error exporting: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/validate-video/{story_id}")
async def validate_video_quality(story_id: str):
    """Run quality checks on generated video"""
    try:
        story = workflow_manager._find_story(story_id)
        if not story or not story.get("video_job_id"):
            raise HTTPException(status_code=404, detail="Video not found")
        job = job_manager.get_job(story["video_job_id"])
        if not job or not job.get("output_file"):
            raise HTTPException(status_code=404, detail="Output not found")
        report = workflow_manager.validate_video_quality(job["output_file"])
        return {
            "story_id": story_id,
            "video_path": job["output_file"],
            "quality_report": report,
        }
    except Exception as e:
        logger.error(f"Error validating: {e}")
        raise HTTPException(status_code=500, detail=str(e))

        if not success:
            raise HTTPException(status_code=404, detail="Story not found")
        return {"success": True, "story_id": story_id}
    except Exception as e:
        logger.error(f"❌ Edit failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    story_ids: Optional[List[str]] = None
