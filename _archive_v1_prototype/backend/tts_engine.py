"""tts_engine.py - Text-to-Speech engine for generating audio"""
import os
from pathlib import Path
from typing import Optional
import logging
import subprocess

logger = logging.getLogger(__name__)

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logger.warning("pyttsx3 not installed. TTS support disabled.")


class TTSEngine:
    """Generate speech audio from text"""
    
    def __init__(self, output_folder: Path):
        self.output_folder = output_folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        if TTS_AVAILABLE:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', 0.9)  # Volume
        else:
            self.engine = None
    
    def generate_audio(self, text: str, output_file: Path, voice_id: int = 0) -> bool:
        """
        Generate audio from text
        voice_id: 0 for male, 1 for female (if available)
        """
        if not TTS_AVAILABLE:
            logger.error("pyttsx3 not available")
            return False
        
        try:
            # Set voice
            voices = self.engine.getProperty('voices')
            if voice_id < len(voices):
                self.engine.setProperty('voice', voices[voice_id].id)
            
            # Generate audio
            self.engine.save_to_file(text, str(output_file))
            self.engine.runAndWait()
            
            if output_file.exists():
                logger.info(f"Generated audio: {output_file}")
                return True
            else:
                logger.error(f"Failed to generate audio: {output_file}")
                return False
        
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            return False
    
    def get_audio_duration(self, audio_file: Path) -> Optional[float]:
        """Get duration of audio file in seconds using ffprobe"""
        try:
            result = subprocess.run(
                [
                    'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1',
                    str(audio_file)
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
        except Exception as e:
            logger.error(f"Failed to get audio duration: {e}")
        
        return None
    
    def concatenate_audio_files(self, audio_files: list, output_file: Path) -> bool:
        """Concatenate multiple audio files into one"""
        try:
            if not audio_files:
                logger.error("No audio files to concatenate")
                return False
            
            # Create concat file for ffmpeg
            concat_file = self.output_folder / "concat_list.txt"
            with open(concat_file, 'w') as f:
                for audio_file in audio_files:
                    f.write(f"file '{audio_file}'\n")
            
            # Concatenate using ffmpeg
            result = subprocess.run(
                [
                    'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                    '-i', str(concat_file), '-c', 'copy', str(output_file)
                ],
                capture_output=True,
                timeout=300
            )
            
            # Clean up
            concat_file.unlink()
            
            if result.returncode == 0 and output_file.exists():
                logger.info(f"Concatenated {len(audio_files)} audio files to {output_file}")
                return True
            else:
                logger.error(f"FFmpeg concat failed: {result.stderr.decode()}")
                return False
        
        except Exception as e:
            logger.error(f"Error concatenating audio: {e}")
            return False
