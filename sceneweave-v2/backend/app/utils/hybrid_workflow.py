"""
hybrid_workflow.py - Hybrid curation + auto-generation system
Manual review + batch auto-processing for $2-5 tier videos
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class CurationStatus(str, Enum):
    """Status of curated content"""
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class HybridWorkflowManager:
    """
    Manages hybrid workflow:
    1. CURATORS: Manually select/edit stories
    2. BATCH PROCESSOR: Auto-generates videos from approved stories
    3. QUALITY: Automated checks before publishing
    """

    def __init__(self, job_manager, lean_processor, db_path: Path = None):
        """Initialize workflow manager"""
        self.job_manager = job_manager
        self.processor = lean_processor
        self.db_path = db_path or Path("/tmp/sceneweave/curated_stories.json")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._load_database()

    def _load_database(self):
        """Load curated stories database"""
        if self.db_path.exists():
            try:
                with open(self.db_path, "r") as f:
                    self.database = json.load(f)
                logger.info(f"✅ Loaded {len(self.database.get('stories', []))} stories")
            except Exception as e:
                logger.warning(f"Database load failed: {e}")
                self.database = {"stories": [], "batches": []}
        else:
            self.database = {"stories": [], "batches": []}

    def _save_database(self):
        """Persist database to disk"""
        try:
            with open(self.db_path, "w") as f:
                json.dump(self.database, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save database: {e}")

    # ====== CURATOR WORKFLOW (Manual) ======

    def submit_story_for_review(
        self,
        story_text: str,
        title: str,
        source: str = "manual",
        tags: List[str] = None,
    ) -> str:
        """Curator submits story for review"""
        if len(story_text) > 500:
            story_text = story_text[:500]

        story_id = f"story_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        story = {
            "id": story_id,
            "title": title,
            "text": story_text,
            "length": len(story_text),
            "source": source,
            "tags": tags or [],
            "status": CurationStatus.PENDING_REVIEW,
            "submitted_at": datetime.utcnow().isoformat(),
            "reviewed_at": None,
            "reviewer_notes": None,
            "video_job_id": None,
        }

        self.database["stories"].append(story)
        self._save_database()
        logger.info(f"📝 Story submitted: {story_id}")
        return story_id

    def review_story(
        self,
        story_id: str,
        approved: bool,
        notes: str = None,
    ) -> bool:
        """Curator reviews and approves/rejects story"""
        story = self._find_story(story_id)
        if not story:
            return False

        story["status"] = CurationStatus.APPROVED if approved else CurationStatus.REJECTED
        story["reviewed_at"] = datetime.utcnow().isoformat()
        story["reviewer_notes"] = notes
        self._save_database()

        logger.info(f"{'✅ APPROVED' if approved else '❌ REJECTED'}: {story_id}")
        return True

    def edit_story(self, story_id: str, updates: Dict) -> bool:
        """Curator edits story before processing"""
        story = self._find_story(story_id)
        if not story:
            return False

        if "text" in updates and len(updates["text"]) > 500:
            updates["text"] = updates["text"][:500]

        story.update(updates)
        self._save_database()
        logger.info(f"✏️ Story edited: {story_id}")
        return True

    def list_pending_stories(self) -> List[Dict]:
        """Get all stories awaiting curator review"""
        return [
            s
            for s in self.database["stories"]
            if s["status"] == CurationStatus.PENDING_REVIEW
        ]


    # ====== BATCH PROCESSING WORKFLOW (Auto) ======

    def create_processing_batch(
        self, batch_name: str, story_ids: List[str] = None
    ) -> str:
        """Create batch of approved stories for video generation"""
        if story_ids is None:
            approved = self.list_approved_stories()
            story_ids = [s["id"] for s in approved]

        if not story_ids:
            logger.warning("No approved stories for batch")
            return None

        batch_id = f"batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        batch = {
            "id": batch_id,
            "name": batch_name,
            "story_ids": story_ids,
            "total_stories": len(story_ids),
            "status": "created",
            "created_at": datetime.utcnow().isoformat(),
            "started_at": None,
            "completed_at": None,
            "results": [],
        }

        self.database["batches"].append(batch)
        self._save_database()
        logger.info(f"📦 Batch created: {batch_id} ({len(story_ids)} stories)")
        return batch_id

    def process_batch(self, batch_id: str) -> Dict:
        """Process entire batch: Generate videos for all approved stories"""
        batch = self._find_batch(batch_id)
        if not batch:
            logger.error(f"Batch not found: {batch_id}")
            return None

        logger.info(f"🎬 Starting batch processing: {batch_id}")
        batch["status"] = "processing"
        batch["started_at"] = datetime.utcnow().isoformat()
        self._save_database()

        results = {
            "batch_id": batch_id,
            "total": len(batch["story_ids"]),
            "completed": 0,
            "failed": 0,
            "videos": [],
        }

        for idx, story_id in enumerate(batch["story_ids"]):
            story = self._find_story(story_id)
            if not story:
                results["failed"] += 1
                continue

            try:
                job_id = f"{batch_id}_{idx:03d}"
                temp_file = self._create_temp_file(story)
                
                logger.info(f"[{batch_id}] Processing {idx + 1}/{len(batch['story_ids'])}")
                success = self.processor.process_story(job_id, temp_file)

                if success:
                    job = self.job_manager.get_job(job_id)
                    story["status"] = CurationStatus.COMPLETED
                    story["video_job_id"] = job_id
                    results["completed"] += 1
                    results["videos"].append({
                        "story_id": story_id,
                        "job_id": job_id,
                        "output": job.get("output_file"),
                    })
                    logger.info(f"✅ Video generated: {job_id}")
                else:
                    results["failed"] += 1
                    story["status"] = CurationStatus.FAILED
                    logger.error(f"❌ Video failed: {story_id}")

            except Exception as e:
                logger.error(f"❌ Error for {story_id}: {e}")
                results["failed"] += 1
                story["status"] = CurationStatus.FAILED

            self._save_database()

        batch["status"] = "completed"
        batch["completed_at"] = datetime.utcnow().isoformat()
        batch["results"] = results
        self._save_database()

        logger.info(f"✅ Batch complete: {results['completed']}/{results['total']} videos")
        return results

    def process_batch_async(self, batch_id: str, background_tasks) -> Dict:
        """Process batch in background (for API)"""
        batch = self._find_batch(batch_id)
        if not batch:
            return {"error": "Batch not found"}

        background_tasks.add_task(self.process_batch, batch_id)
        return {
            "batch_id": batch_id,
            "status": "processing",
            "message": f"Batch queued for processing",
        }

    # ====== QUALITY CHECKS (Automated) ======

    def validate_video_quality(self, video_path: str) -> Dict:
        """Automated quality checks on generated video"""
        report = {"video_path": video_path, "checks": {}, "passes": True}

        try:
            import subprocess
            from pathlib import Path

            video = Path(video_path)

            # Check 1: File exists and has reasonable size
            if not video.exists():
                report["checks"]["file_exists"] = False
                report["passes"] = False
            else:
                size_mb = video.stat().st_size / (1024 * 1024)
                report["checks"]["file_size_mb"] = size_mb
                report["checks"]["file_exists"] = True

                if size_mb < 1 or size_mb > 50:
                    report["checks"]["file_size_valid"] = False
                    report["passes"] = False
                else:
                    report["checks"]["file_size_valid"] = True

            # Check 2: Video duration
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", video_path],
                capture_output=True, text=True, timeout=5,
            )

            duration = int(float(result.stdout.strip()))
            report["checks"]["duration_seconds"] = duration

            if duration < 45 or duration > 90:
                report["checks"]["duration_valid"] = False
                report["passes"] = False
            else:
                report["checks"]["duration_valid"] = True

        except Exception as e:
            logger.warning(f"Quality check failed: {e}")
            report["checks"]["error"] = str(e)
            report["passes"] = False

        return report

    # ====== HELPER METHODS ======

    def _find_story(self, story_id: str) -> Optional[Dict]:
        """Find story by ID"""
        for story in self.database["stories"]:
            if story["id"] == story_id:
                return story
        return None

    def _find_batch(self, batch_id: str) -> Optional[Dict]:
        """Find batch by ID"""
        for batch in self.database["batches"]:
            if batch["id"] == batch_id:
                return batch
        return None

    def _create_temp_file(self, story: Dict) -> str:
        """Create temporary story file for processing"""
        temp_file = Path("/tmp/sceneweave/temp") / f"{story['id']}.txt"
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file.write_text(story["text"])
        return str(temp_file)

    def get_stats(self) -> Dict:
        """Get workflow statistics"""
        stories = self.database["stories"]
        batches = self.database["batches"]

        return {
            "total_stories": len(stories),
            "pending_review": len([s for s in stories if s["status"] == CurationStatus.PENDING_REVIEW]),
            "approved": len([s for s in stories if s["status"] == CurationStatus.APPROVED]),
            "completed": len([s for s in stories if s["status"] == CurationStatus.COMPLETED]),
            "failed": len([s for s in stories if s["status"] == CurationStatus.FAILED]),
            "total_batches": len(batches),
            "batches_completed": len([b for b in batches if b["status"] == "completed"]),
            "total_videos_generated": len([s for s in stories if s["video_job_id"]]),
        }

    def export_batch_videos(self, batch_id: str, output_dir: str = None) -> List[str]:
        """Export all videos from batch to directory"""
        batch = self._find_batch(batch_id)
        if not batch:
            return []

        export_dir = Path(output_dir) if output_dir else Path("/tmp/sceneweave/exports")
        export_dir.mkdir(parents=True, exist_ok=True)

        exported = []
        for result in batch.get("results", {}).get("videos", []):
            src = Path(result["output"])
            if src.exists():
                dst = export_dir / f"{result['story_id']}.mp4"
                import shutil
                shutil.copy(src, dst)
                exported.append(str(dst))

        logger.info(f"📦 Exported {len(exported)} videos from {batch_id}")
        return exported


    def list_approved_stories(self) -> List[Dict]:
        """Get all curator-approved stories ready for processing"""
        return [
            s
            for s in self.database["stories"]
            if s["status"] == CurationStatus.APPROVED and not s["video_job_id"]
        ]
