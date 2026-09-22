"""
processor.py - Background job processing orchestrator
"""
import logging
from pathlib import Path
from app.config import settings
from app.utils.job_manager import JobManager
from app.utils.llm_processor import GroqScriptGenerator, create_generator
from app.utils.tts_engine import KokoroTTSEngine
from app.utils.video_composer import FFmpegVideoComposer
from app.utils.logger import setup_logging
from PIL import Image

# Use centralized logging setup
logger = setup_logging(settings.LOGS_DIR, app_name="sceneweave-worker")

job_manager = JobManager()
script_gen = None  # Lazy init - will be initialized on first use
tts = KokoroTTSEngine(settings.OUTPUT_DIR)
composer = FFmpegVideoComposer(settings.OUTPUT_DIR, settings.TEMP_DIR)

def get_script_generator():
    """Get or create script generator (lazy initialization)"""
    global script_gen
    if script_gen is None:
        try:
            logger.info(f"[{__name__}] Creating GroqScriptGenerator instance...")
            # Directly instantiate - let GroqScriptGenerator handle API key logic
            script_gen = GroqScriptGenerator()
            logger.info(f"[{__name__}] ✅ GroqScriptGenerator created successfully")
        except Exception as e:
            logger.error(f"[{__name__}] ❌ GroqScriptGenerator creation failed: {type(e).__name__}: {e}")
            return None
    
    return script_gen

async def process_job(job_id: str, file_path: str):
    """Process job through all phases"""
    try:
        job_manager.update_job(job_id, status="processing", progress=0, message="Reading...")
        
        with open(file_path, 'r') as f:
            text = f.read()
        
        logger.info(f"[{job_id}] ========== Processing Started ==========")
        logger.info(f"[{job_id}] Input text: {len(text)} characters")
        
        # Truncate text if too large for Groq API (max ~10k tokens ≈ 40KB)
        max_text_length = 15000  # Conservative limit to avoid 413 errors
        if len(text) > max_text_length:
            logger.warning(f"[{job_id}] Text truncated from {len(text)} to {max_text_length} chars (file too large for Groq)")
            text = text[:max_text_length] + "\n[... text truncated for API limits ...]"
        
        logger.info(f"[{job_id}] Phase 2: LLM screenplay")
        job_manager.update_job(job_id, progress=20, message="Generating screenplay...")
        
        script = None
        try:
            gen = get_script_generator()
            if gen is None:
                logger.error(f"[{job_id}] ❌ Groq generator is None - will use placeholder")
                script = _placeholder_script(text)
            else:
                logger.info(f"[{job_id}] Calling Groq to generate screenplay...")
                script = gen.generate_script(text, job_id)
                if script and script.get('scenes'):
                    logger.info(f"[{job_id}] ✅ Groq success: {len(script.get('scenes', []))} scenes generated")
                else:
                    logger.error(f"[{job_id}] ❌ Groq returned empty/invalid script, using placeholder")
                    script = _placeholder_script(text)
        except Exception as e:
            logger.error(f"[{job_id}] ❌ Groq failed with {type(e).__name__}: {str(e)}", exc_info=True)
            script = _placeholder_script(text)
        
        if not script:
            logger.error(f"[{job_id}] ❌ No script generated, using default placeholder")
            script = _placeholder_script(text)
        
        logger.info(f"[{job_id}] Using screenplay with {len(script.get('scenes', []))} scene(s)")
        
        logger.info(f"[{job_id}] Phase 3: TTS audio")
        job_manager.update_job(job_id, progress=40, message="Generating audio...")
        
        scene_videos = []
        for scene_idx, scene in enumerate(script.get("scenes", [])):
            audio_files = []
            for dial_idx, dialogue in enumerate(scene.get("dialogue", [])):
                try:
                    audio = tts.generate_audio(
                        dialogue["text"],
                        dialogue.get("character", "narrator"),
                        dialogue.get("emotion", "neutral"),
                        job_id, scene_idx, dial_idx
                    )
                    audio_files.append(audio)
                except Exception as e:
                    logger.warning(f"[{job_id}] Scene {scene_idx} dialogue {dial_idx} audio FAILED: {e}")
            
            merged = str(settings.OUTPUT_DIR / f"{job_id}_s{scene_idx}.wav")
            if audio_files:
                logger.info(f"[{job_id}] Scene {scene_idx}: Merging {len(audio_files)} audio files")
                tts.merge_audio_files(audio_files, merged)
            else:
                logger.info(f"[{job_id}] Scene {scene_idx}: No dialogue, creating silent audio")
                tts._create_silent_audio(merged, 5)
            
            duration = scene.get("duration_seconds", 30)  # Changed default from 10 to 30
            logger.info(f"[{job_id}] Phase 4: Video scene {scene_idx}")
            job_manager.update_job(job_id, progress=40 + (40 * scene_idx / max(len(script.get("scenes", [])), 1)),
                                 message=f"Video scene {scene_idx + 1}...")
            
            try:
                bg = _get_background(scene.get("background", "default"))
                logger.info(f"[{job_id}] Scene {scene_idx}: bg={bg}, duration={duration}s, audio={merged}")
                video = composer.compose_scene_video(bg, [], merged, 
                                                    duration,
                                                    job_id, scene_idx)
                logger.info(f"[{job_id}] ✅ Scene {scene_idx}: Video created: {video}")
                scene_videos.append(video)
            except Exception as e:
                logger.error(f"[{job_id}] ❌ Scene {scene_idx} Video FAILED: {e}", exc_info=True)
        
        if scene_videos:
            final = str(settings.OUTPUT_DIR / f"{job_id}_final.mp4")
            try:
                composer.concatenate_videos(scene_videos, final, job_id)
                job_manager.update_job(job_id, status="completed", progress=100,
                                     message="Complete!", output_file=final)
                logger.info(f"[{job_id}] ========== Job COMPLETED ==========")
            except Exception as e:
                logger.warning(f"[{job_id}] Concatenation failed, using first scene: {e}")
                job_manager.update_job(job_id, status="completed", progress=100,
                                     message="Partial", output_file=scene_videos[0])
        else:
            logger.error(f"[{job_id}] ❌ No scene videos generated")
            job_manager.update_job(job_id, status="failed", progress=0,
                                 message="No videos", error="Scene processing failed")
    
    except Exception as e:
        logger.error(f"[{job_id}] ========== FATAL ERROR ==========")
        logger.error(f"[{job_id}] {type(e).__name__}: {e}", exc_info=True)
        job_manager.update_job(job_id, status="failed", progress=0,
                             message="Failed", error=str(e))

def _placeholder_script(text: str) -> dict:
    """Generate a better placeholder script when Groq is unavailable"""
    # Extract meaningful content from the text
    lines = text.split('\n')
    
    # Get first non-empty line as title
    title = next((line.strip() for line in lines if line.strip()), "Story")[:100]
    
    # Get first 200 chars as description
    description = text[:200].replace('\n', ' ').strip()
    
    # Split text into paragraphs for scenes (max 3 scenes)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    num_scenes = min(3, max(1, len(paragraphs)))
    
    scenes = []
    chars_per_scene = len(text) // num_scenes
    
    for scene_idx in range(num_scenes):
        start = scene_idx * chars_per_scene
        end = (scene_idx + 1) * chars_per_scene if scene_idx < num_scenes - 1 else len(text)
        scene_text = text[start:end].strip()
        
        # Extract first 1000 chars for this scene
        scene_text = scene_text[:1000]
        
        # Create dialogue lines (split on periods or newlines)
        sentences = [s.strip() for s in scene_text.replace('\n', '. ').split('.') if s.strip()]
        
        # Create 2-3 dialogue entries per scene
        dialogue = []
        for sent_idx, sentence in enumerate(sentences[:3]):
            if sentence:
                dialogue.append({
                    "character": ["Narrator", "Character 1", "Character 2"][sent_idx % 3],
                    "text": sentence + ".",
                    "emotion": "neutral"
                })
        
        if not dialogue:  # Fallback
            dialogue.append({"character": "Narrator", "text": scene_text[:500], "emotion": "neutral"})
        
        # Dynamic duration: at least 15 seconds, scale with content
        duration = max(15, min(60, len(scene_text) // 50))
        
        scenes.append({
            "id": scene_idx + 1,
            "name": f"Scene {scene_idx + 1}",
            "description": scene_text[:200],
            "background": "default",
            "duration_seconds": duration,
            "characters": ["Narrator", "Character 1", "Character 2"],
            "dialogue": dialogue
        })
    
    # Calculate total duration
    total_duration = sum(s.get("duration_seconds", 30) for s in scenes)
    
    return {
        "title": title,
        "scenes": scenes,
        "characters": [
            {"name": "Narrator", "voice_type": "neutral"},
            {"name": "Character 1", "voice_type": "neutral"},
            {"name": "Character 2", "voice_type": "neutral"}
        ],
        "metadata": {"total_duration_seconds": total_duration}
    }

def _get_background(name: str) -> str:
    assets = settings.ASSETS_DIR / "backgrounds"
    bg = assets / f"{name}.png"
    if bg.exists():
        return str(bg)
    
    default = assets / "default.png"
    if not default.exists():
        default.parent.mkdir(parents=True, exist_ok=True)
        Image.new('RGB', (1920, 1080), (173, 216, 230)).save(default)
    
    return str(default)
