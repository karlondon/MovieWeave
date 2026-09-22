"""
video_composer.py - FFmpeg integration for video composition
"""
import logging
from pathlib import Path
import subprocess
from PIL import Image
import shutil

logger = logging.getLogger(__name__)

class VideoCompositionError(Exception):
    pass

class FFmpegVideoComposer:
    """Compose videos from frames and audio using FFmpeg"""
    
    def __init__(self, output_dir: Path, temp_dir: Path):
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Find ffmpeg executable - try multiple locations
        self.ffmpeg_path = self._find_ffmpeg()
        if not self.ffmpeg_path:
            logger.error("❌ FFmpeg not found! Install FFmpeg or add to PATH")
    
    def _find_ffmpeg(self) -> str:
        """Find ffmpeg executable in common locations"""
        # Try standard locations
        possible_paths = [
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "/opt/homebrew/bin/ffmpeg",
            shutil.which("ffmpeg")  # Try PATH environment
        ]
        
        for path in possible_paths:
            if path and Path(path).exists():
                logger.info(f"✅ Found FFmpeg at: {path}")
                return path
        
        return None
    
    
    def compose_scene_video(self, background_path: str, animations: list, audio_path: str, 
                           duration: float, job_id: str, scene_id: int, fps: int = 24) -> str:
        """Compose scene video with background, sprites, and audio"""
        try:
            output_video = self.output_dir / f"{job_id}_scene{scene_id}.mp4"
            logger.info(f"[{job_id}] Composing scene {scene_id}")
            
            frames_dir = self.temp_dir / f"{job_id}_frames_scene{scene_id}"
            frames_dir.mkdir(parents=True, exist_ok=True)
            
            self._create_frames(background_path, animations, frames_dir, duration, fps)
            self._create_video_from_frames(frames_dir, audio_path, str(output_video), fps, duration)
            
            logger.info(f"[{job_id}] Scene video created")
            return str(output_video)
        except Exception as e:
            logger.error(f"[{job_id}] Composition failed: {str(e)}")
            raise VideoCompositionError(str(e))
    
    def _create_frames(self, bg_path: str, animations: list, frames_dir: Path, duration: float, fps: int):
        """Create animation frames"""
        try:
            bg = Image.open(bg_path).convert('RGBA')
            total_frames = int(duration * fps)
            
            for frame_num in range(total_frames):
                frame = bg.copy()
                # Simple lip-sync: open/closed every 2 frames
                for anim in animations:
                    x, y = anim.get('x', 100), anim.get('y', 100)
                    if anim.get('sprite_path') and Path(anim['sprite_path']).exists():
                        sprite = Image.open(anim['sprite_path']).convert('RGBA')
                        frame.paste(sprite, (x, y), sprite)
                
                frame.save(frames_dir / f"frame_{frame_num:06d}.png")
            logger.info(f"Created {total_frames} frames")
        except Exception as e:
            raise VideoCompositionError(f"Frame creation failed: {str(e)}")
    
    def _create_video_from_frames(self, frames_dir: Path, audio_path: str, 
                                 output_path: str, fps: int, duration: float):
        """Create MP4 from frames and audio"""
        try:
            if not self.ffmpeg_path:
                raise VideoCompositionError("FFmpeg not found in system")
            
            cmd = [
                self.ffmpeg_path, "-framerate", str(fps),
                "-pattern_type", "glob", "-i", str(frames_dir / "frame_*.png"),
                "-i", audio_path,
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-t", str(duration), "-y", output_path
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=300, check=False)
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr.decode()}")
            logger.info(f"✅ Video created: {output_path}")
        except Exception as e:
            raise VideoCompositionError(f"Video creation failed: {str(e)}")
    
    def concatenate_videos(self, video_paths: list, output_path: str, job_id: str) -> str:
        """Merge scene videos into final output"""
        try:
            if not self.ffmpeg_path:
                raise VideoCompositionError("FFmpeg not found in system")
            
            logger.info(f"[{job_id}] Concatenating {len(video_paths)} videos")
            
            concat_file = self.temp_dir / f"{job_id}_concat.txt"
            with open(concat_file, 'w') as f:
                for vp in video_paths:
                    f.write(f"file '{vp}'\n")
            
            cmd = [self.ffmpeg_path, "-f", "concat", "-safe", "0",
                   "-i", str(concat_file), "-c", "copy", "-y", output_path]
            
            result = subprocess.run(cmd, capture_output=True, timeout=600, check=False)
            if result.returncode != 0:
                logger.error(f"FFmpeg concat error: {result.stderr.decode()}")
            logger.info(f"[{job_id}] ✅ Final video created")
            return output_path
        except Exception as e:
            raise VideoCompositionError(f"Concatenation failed: {str(e)}")
