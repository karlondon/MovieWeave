"""
lean_processor.py - Cost-optimized video generation for $2-5 tier
Handles 500-char max stories → 60-90 second professional videos
Integrates with existing job_manager, tts_engine, and video_composer
"""
import logging
from pathlib import Path
from app.config import settings

logger = logging.getLogger(__name__)


class LeanVideoProcessor:
    """
    Optimized processor for short-form videos ($2-5 price tier)
    - Input: 500-char stories
    - Output: 60-90 second MP4 videos
    - Cost per video: ~$0.15-0.30
    """

    def __init__(self, job_manager, tts_engine, video_composer, llm_generator=None):
        """
        Initialize processor with required dependencies
        
        Args:
            job_manager: JobManager instance for tracking progress
            tts_engine: KokoroTTSEngine instance for audio generation
            video_composer: FFmpegVideoComposer instance
            llm_generator: Optional GroqScriptGenerator for enhanced analysis
        """
        self.job_manager = job_manager
        self.tts = tts_engine
        self.composer = video_composer
        self.llm = llm_generator

    def process_story(self, job_id: str, file_path: str) -> bool:
        """
        Main entry point: Convert story to professional video
        
        Args:
            job_id: Unique job identifier
            file_path: Path to text file containing story
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Phase 1: Read and validate story (5%)
            self.job_manager.update_job(
                job_id, status="processing", progress=5, message="Reading story..."
            )

            with open(file_path, "r") as f:
                story_text = f.read().strip()

            if not story_text:
                logger.error(f"[{job_id}] Empty story file")
                self.job_manager.update_job(
                    job_id,
                    status="failed",
                    progress=0,
                    message="Empty file",
                    error="Story file is empty",
                )
                return False

            # Enforce 500-char limit
            if len(story_text) > 500:
                logger.warning(f"[{job_id}] Story truncated from {len(story_text)} to 500 chars")
                story_text = story_text[:500]

            logger.info(f"[{job_id}] Processing {len(story_text)}-char story")

            # Phase 2: Analyze story essence (15%)
            self.job_manager.update_job(job_id, progress=15, message="Analyzing...")
            story_data = self._analyze_story(story_text, job_id)

            # Phase 3: Select visuals (5%)
            self.job_manager.update_job(job_id, progress=20, message="Selecting visuals...")
            bg_path = self._select_background(story_data)

            # Phase 4: Generate audio (50%)
            self.job_manager.update_job(job_id, progress=25, message="Generating audio...")
            audio_file = self._generate_audio(story_text, job_id)

            if not audio_file:
                logger.error(f"[{job_id}] Audio generation failed")
                self.job_manager.update_job(
                    job_id,
                    status="failed",
                    progress=0,
                    message="Audio failed",
                    error="Could not generate audio",
                )
                return False

            # Phase 5: Compose video (20%)
            self.job_manager.update_job(job_id, progress=75, message="Creating video...")
            video_file = self._compose_video(bg_path, audio_file, job_id)

            if not video_file:
                logger.error(f"[{job_id}] Video composition failed")
                self.job_manager.update_job(
                    job_id,
                    status="failed",
                    progress=0,
                    message="Video failed",
                    error="Could not compose video",
                )
                return False

            # Success!
            self.job_manager.update_job(
                job_id,
                status="completed",
                progress=100,
                message="Done! Professional 60-90s video created",
                output_file=video_file,
            )

            logger.info(f"[{job_id}] ✅ Complete: {video_file}")
            return True

        except Exception as e:
            logger.error(f"[{job_id}] Processing failed: {e}", exc_info=True)
            self.job_manager.update_job(
                job_id,
                status="failed",
                progress=0,
                message="Processing failed",
                error=str(e),
            )

    def _analyze_story(self, story_text: str, job_id: str) -> dict:
        """Analyze story to extract tone, setting, and key elements"""
        analysis = {
            "tone": self._detect_tone(story_text),
            "setting": self._detect_setting(story_text),
            "length": len(story_text),
        }
        if self.llm:
            try:
                prompt = f"""Analyze (JSON only): {story_text[:250]}"""
                response = self.llm._call_groq(prompt)
                llm_data = self.llm._parse_response(response, job_id)
                analysis.update(llm_data)
            except Exception as e:
                logger.warning(f"[{job_id}] LLM analysis skipped: {e}")
        return analysis

    def _detect_tone(self, text: str) -> str:
        """Detect story tone from keywords"""
        text_lower = text.lower()
        if any(w in text_lower for w in ["happy", "love", "joy", "wonderful"]):
            return "happy"
        if any(w in text_lower for w in ["dark", "scary", "fear", "danger"]):
            return "dark"
        if any(w in text_lower for w in ["mystery", "secret", "hidden"]):
            return "mysterious"
        if any(w in text_lower for w in ["adventure", "journey", "explore"]):
            return "exciting"
        return "neutral"

    def _detect_setting(self, text: str) -> str:
        """Detect story setting from keywords"""
        text_lower = text.lower()
        if "forest" in text_lower or "woods" in text_lower:
            return "forest"
        if "beach" in text_lower or "ocean" in text_lower:
            return "beach"
        if "castle" in text_lower or "kingdom" in text_lower:
            return "castle"
        if "city" in text_lower or "town" in text_lower:
            return "city"
        if "space" in text_lower or "planet" in text_lower:
            return "space"
        return "fantasy"

    def _select_background(self, story_data: dict) -> str:
        """Select background image based on story setting"""
        setting = story_data.get("setting", "fantasy").lower()
        bg_map = {"forest": "forest", "beach": "beach", "castle": "library",
                  "city": "office", "space": "night"}
        bg_name = bg_map.get(setting, "default")
        bg_file = settings.ASSETS_DIR / "backgrounds" / f"{bg_name}.jpg"
        if bg_file.exists():
            return str(bg_file)
        default_bg = settings.ASSETS_DIR / "backgrounds" / "default.jpg"
        return str(default_bg) if default_bg.exists() else None

    def _generate_audio(self, story_text: str, job_id: str) -> str:
        """Generate narration audio from story"""
        try:
            audio_file = self.tts.generate_audio(
                text=story_text[:500],
                character="narrator",
                emotion="neutral",
                job_id=job_id,
                scene_id=0,
                dialogue_id=0,
            )
            if audio_file and Path(audio_file).exists():
                return audio_file
            return None
        except Exception as e:
            logger.error(f"[{job_id}] Audio failed: {e}")
            return None

    def _compose_video(self, bg_path: str, audio_file: str, job_id: str) -> str:
        """Compose final video from background and audio"""
        try:
            if not bg_path:
                return None
            video_file = str(settings.OUTPUT_DIR / f"{job_id}_final.mp4")
            duration = self._get_audio_duration(audio_file, job_id)
            if duration is None:
                duration = 60
            duration = max(45, min(90, duration))
            video = self.composer.compose_scene_video(
                background_path=bg_path,
                animations=[],
                audio_path=audio_file,
                duration=duration,
                job_id=job_id,
                scene_id=0,
            )
            if video and Path(video).exists():
                return video
            return None
        except Exception as e:
            logger.error(f"[{job_id}] Video composition failed: {e}")
            return None

    def _get_audio_duration(self, audio_file: str, job_id: str) -> int:
        """Get duration of audio file in seconds"""
        try:
            import subprocess
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", audio_file],
                capture_output=True, text=True, timeout=5,
            )
            return int(float(result.stdout.strip()))
        except Exception as e:
            logger.warning(f"[{job_id}] Could not get duration: {e}")
            return None

            return False
