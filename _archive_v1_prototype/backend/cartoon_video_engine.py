"""CartoonVideoEngine - Generate animated cartoon videos with lip-sync"""
from pathlib import Path
import subprocess
import logging
from backend.character_manager import CharacterManager
from backend.lip_sync_engine import LipSyncEngine

logger = logging.getLogger(__name__)

class CartoonVideoEngine:
    """Generate cartoon videos from character frames using FFmpeg"""
    
    FPS = 24
    VIDEO_CODEC = 'libx264'
    PRESET = 'medium'
    CRF = 23
    
    def __init__(self, character_dir: Path = None, output_dir: Path = None):
        if character_dir is None:
            character_dir = Path("backend/assets/characters")
        if output_dir is None:
            output_dir = Path("output/videos")
        
        self.character_dir = Path(character_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.manager = CharacterManager(self.character_dir)
        self.engine = LipSyncEngine()
    
    def render_dialogue_video(self, character_name: str, expression: str = 'neutral',
                             duration_seconds: float = 3.0, audio_file: Path = None,
                             output_file: Path = None) -> bool:
        """Render character dialogue video with lip-sync"""
        try:
            character = self.manager.load_character(character_name)
            if not character:
                logger.error(f"Character not found: {character_name}")
                return False
            
            if output_file is None:
                output_file = self.output_dir / f"{character_name}_dialogue.mp4"
            
            frame_dir = self.output_dir / f"{character_name}_frames"
            frame_dir.mkdir(parents=True, exist_ok=True)
            
            if audio_file:
                self.engine.load_audio(audio_file)
            self.engine.extract_mouth_shapes()
            
            frame_count = int(duration_seconds * self.FPS)
            
            for frame_num in range(frame_count):
                time = frame_num / self.FPS
                mouth_shape = self.engine.get_mouth_at_time(time)
                frame = character.render_frame(expression=expression, mouth_shape=mouth_shape)
                frame.save(frame_dir / f"frame_{frame_num:06d}.png")
            
            return self._encode_video(frame_dir, output_file, audio_file)
            
        except Exception as e:
            logger.error(f"Failed to render dialogue: {e}")
            return False
    
    def render_rotating_character_video(self, dialogue_lines: list, characters: list,
                                       expression: str = 'happy', audio_files: list = None,
                                       durations: list = None, output_file: Path = None) -> bool:
        """Render video with rotating characters, each speaking one line"""
        try:
            if not dialogue_lines or not characters:
                logger.error("No dialogue lines or characters provided")
                return False
            
            if output_file is None:
                output_file = self.output_dir / "rotating_chars_video.mp4"
            
            all_frames_dir = self.output_dir / "rotating_frames_temp"
            all_frames_dir.mkdir(parents=True, exist_ok=True)
            
            frame_counter = 0
            
            # Process each dialogue line
            for idx, line in enumerate(dialogue_lines):
                char_name = characters[idx % len(characters)]
                duration = durations[idx] if durations and idx < len(durations) else 2.0
                audio_file = audio_files[idx] if audio_files and idx < len(audio_files) else None
                
                logger.info(f"Scene {idx+1}/{len(dialogue_lines)}: {char_name} ({duration:.2f}s)")
                
                character = self.manager.load_character(char_name)
                if not character:
                    logger.warning(f"Character not found: {char_name}")
                    continue
                
                frame_count = int(duration * self.FPS)
                
                if audio_file and Path(audio_file).exists():
                    self.engine.load_audio(audio_file)
                    self.engine.extract_mouth_shapes()
                
                for frame_num in range(frame_count):
                    time = frame_num / self.FPS
                    mouth_shape = self.engine.get_mouth_at_time(time) if audio_file else 'neutral'
                    frame = character.render_frame(expression=expression, mouth_shape=mouth_shape)
                    frame_path = all_frames_dir / f"frame_{frame_counter:06d}.png"
                    frame.save(frame_path)
                    frame_counter += 1
            
            if frame_counter > 0:
                logger.info(f"Encoding {frame_counter} frames to video...")
                return self._encode_video(all_frames_dir, output_file)
            else:
                logger.error("No frames generated")
                return False
            
        except Exception as e:
            logger.error(f"Failed to render rotating character video: {e}")
            return False


    
    def _encode_video(self, frame_dir: Path, output_file: Path, 
                     audio_file: Path = None) -> bool:
        """Encode frames to MP4 using FFmpeg"""
        try:
            cmd = [
                'ffmpeg', '-framerate', str(self.FPS),
                '-i', str(frame_dir / 'frame_%06d.png'),
                '-c:v', self.VIDEO_CODEC, '-preset', self.PRESET,
                '-crf', str(self.CRF), '-y', str(output_file)
            ]
            
            if audio_file and Path(audio_file).exists():
                cmd.insert(4, '-i')
                cmd.insert(5, str(audio_file))
                cmd.extend(['-c:a', 'aac', '-shortest'])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except FileNotFoundError:
            logger.error("FFmpeg not found. Install: brew install ffmpeg")
            return False
