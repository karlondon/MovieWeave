"""
enhanced_video_composer.py - Render animated videos
Minimal, focused implementation for composing videos from assets
"""
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
import subprocess
import shutil

logger = logging.getLogger(__name__)

class EnhancedVideoComposer:
    def __init__(self, output_dir: Path, temp_dir: Path):
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.ffmpeg = self._find_ffmpeg()
        self.fps = 24
    
    def _find_ffmpeg(self) -> Optional[str]:
        paths = ["/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg", 
                 "/opt/homebrew/bin/ffmpeg", shutil.which("ffmpeg")]
        for p in paths:
            if p and Path(p).exists():
                return p
        return None
    
    def compose_video(self, job_id: str, bg_path: str, audio_path: str, 
                     duration_sec: float, char_sprites: Dict = None) -> str:
        """Simple video composition: background + audio"""
        try:
            logger.info(f"[{job_id}] Composing video")
            if not self.ffmpeg or not Path(bg_path).exists():
                raise Exception("FFmpeg or background missing")
            
            frames_dir = self._render_frames(job_id, bg_path, duration_sec)
            video_path = self._create_video(job_id, frames_dir, audio_path, duration_sec)
            
            logger.info(f"[{job_id}] ✅ Video ready: {video_path}")
            return str(video_path)
        except Exception as e:
            logger.error(f"[{job_id}] Failed: {str(e)}")
            raise
    
    def _render_frames(self, job_id: str, bg_path: str, duration_sec: float) -> Path:
        """Create frame sequence from background"""
        try:
            from PIL import Image
        except:
            logger.error("PIL required")
            return None
        
        frames_dir = self.temp_dir / job_id / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            bg = Image.open(bg_path).convert('RGBA')
        except:
            bg = Image.new('RGBA', (1920, 1080), (100, 150, 200, 255))
        
        total_frames = int(duration_sec * self.fps)
        
        for i in range(total_frames):
            bg.save(frames_dir / f"frame_{i:06d}.png")
        
        return frames_dir
    
    def _create_video(self, job_id: str, frames_dir: Path, 
                     audio_path: str, duration_sec: float) -> Path:
        """Create MP4 from frames + audio"""
        out = self.output_dir / f"{job_id}_final.mp4"
        
        cmd = [
            self.ffmpeg, "-framerate", str(self.fps),
            "-pattern_type", "glob", "-i", str(frames_dir / "frame_*.png"),
            "-i", audio_path, "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", "-y", str(out)
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=600, check=False)
     
    def _fallback_bg(self) -> Optional[str]:
        """Create fallback background"""
        try:
            from PIL import Image
            bg = self.temp_dir / "fallback.png"
            Image.new('RGB', (1920, 1080), (100, 150, 200)).save(bg)
            return str(bg)
        except:
            return None
    
    def _silent_audio(self, duration: float) -> Optional[str]:
        """Create silent audio"""
        try:
            import numpy as np
            import soundfile as sf
            audio = self.temp_dir / "silent.wav"
            samples = np.zeros(int(22050 * duration))
            sf.write(str(audio), samples, 22050)
            return str(audio)
        except:
            return None

        return out if result.returncode == 0 else None
