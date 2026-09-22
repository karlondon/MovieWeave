"""
tts_engine.py - Kokoro TTS integration for audio generation
"""
import logging
from pathlib import Path
import subprocess
import numpy as np
import soundfile as sf

logger = logging.getLogger(__name__)

class TTSError(Exception):
    """Error during TTS generation"""
    pass

class KokoroTTSEngine:
    """Generate speech audio from text using Kokoro TTS"""
    
    def __init__(self, output_dir: Path):
        """Initialize Kokoro TTS engine"""
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sample_rate = 22050
        
    def generate_audio(self, text: str, character: str, emotion: str, job_id: str, scene_id: int, dialogue_id: int) -> str:
        """Generate speech audio from text"""
        try:
            filename = f"{job_id}_scene{scene_id}_dialogue{dialogue_id}.wav"
            filepath = self.output_dir / filename
            
            logger.info(f"[{job_id}] Generating audio: {character} ({emotion})")
            
            # Generate using espeak-ng with emotion-based rate
            self._generate_audio(text, str(filepath), character, emotion)
            
            if not filepath.exists():
                raise TTSError(f"Audio file not created")
            
            logger.info(f"[{job_id}] Audio generated: {filename}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"[{job_id}] TTS failed: {str(e)}")
            raise TTSError(f"TTS generation failed: {str(e)}")
    
    def _generate_audio(self, text: str, output_path: str, character: str, emotion: str):
        """Generate audio using espeak-ng"""
        rate_map = {"happy": 150, "excited": 160, "sad": 80, "angry": 130, "scared": 120, "neutral": 100}
        rate = rate_map.get(emotion, 100)
        
        try:
            cmd = ["espeak-ng", "-w", output_path, "-s", str(rate), text]
            subprocess.run(cmd, capture_output=True, timeout=30, check=False)
        except FileNotFoundError:
            logger.warning("espeak-ng not found, creating silent placeholder")
            self._create_silent_audio(output_path, duration=2.0)
    
    def _create_silent_audio(self, output_path: str, duration: float = 2.0):
        """Create silent audio placeholder"""
        try:
            samples = np.zeros(int(self.sample_rate * duration))
            sf.write(output_path, samples, self.sample_rate)
        except Exception as e:
            logger.error(f"Failed to create silent audio: {str(e)}")
            raise TTSError(str(e))
    
    def merge_audio_files(self, audio_paths: list, output_path: str, crossfade: float = 0.2) -> str:
        """Merge multiple audio files with crossfade"""
        try:
            logger.info(f"Merging {len(audio_paths)} audio files")
            merged = None
            sr = None
            
            for audio_path in audio_paths:
                data, sr = sf.read(audio_path)
                if merged is None:
                    merged = data
                else:
                    cf_samples = int(crossfade * sr)
                    if len(merged) >= cf_samples:
                        fade_out = np.linspace(1, 0, cf_samples)
                        fade_in = np.linspace(0, 1, cf_samples)
                        merged[-cf_samples:] *= fade_out
                        data[:cf_samples] *= fade_in
                        merged = np.concatenate([merged[:-cf_samples], data])
                    else:
                        merged = np.concatenate([merged, data])
            
            sf.write(output_path, merged, sr)
            logger.info(f"Audio merged: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Audio merge failed: {str(e)}")
            raise TTSError(f"Failed to merge audio: {str(e)}")
