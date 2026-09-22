"""
Feature 4: Character Animation Builder
Build custom animations frame-by-frame
"""

from pathlib import Path
from datetime import datetime
import shutil
from backend.character_manager import CharacterManager
from backend.cartoon_video_engine import CartoonVideoEngine
from backend.animation_presets import AnimationPresets


class CharacterAnimationBuilder:
    """Build custom animations frame-by-frame"""
    
    def __init__(self, character_name: str):
        self.character_name = character_name
        self.character_manager = CharacterManager(Path('backend/assets/characters'))
        self.character = self.character_manager.load_character(character_name)
        self.frames = []
        
        if not self.character:
            raise ValueError(f"Character {character_name} not found")
    
    def add_frame(self, expression: str, mouth_shape: str, duration_frames: int = 1):
        """Add frame to animation"""
        frame = self.character.render_frame(expression, mouth_shape)
        for _ in range(duration_frames):
            self.frames.append(frame)
        
        return self
    
    def add_animation_preset(self, preset_name: str):
        """Add preset animation sequence"""
        preset_method = f'get_{preset_name}_animation'
        if not hasattr(AnimationPresets, preset_method):
            raise ValueError(f"Preset '{preset_name}' not found")
        
        preset_sequence = getattr(AnimationPresets, preset_method)()
        
        for expr, mouth, count in preset_sequence:
            self.add_frame(expr, mouth, count)
        
        return self
    
    def render_to_video(self, output_file: Path = None, audio_file: Path = None) -> Path:
        """Render animation to MP4 video"""
        if not self.frames:
            raise ValueError("No frames added to animation")
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path('output/videos') / f"{self.character_name}_custom_{timestamp}.mp4"
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save frames to temporary directory
        frame_dir = Path('output/temp_frames') / str(datetime.now().timestamp())
        frame_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            for i, frame in enumerate(self.frames):
                frame.save(frame_dir / f"frame_{i:06d}.png")
            
            # Encode to video
            video_engine = CartoonVideoEngine()
            success = video_engine._encode_video(frame_dir, output_file, audio_file)
            
            return output_file if success else None
            
        finally:
            # Cleanup temp frames
            if frame_dir.exists():
                shutil.rmtree(frame_dir)
    
    def get_frame_count(self):
        """Get total number of frames"""
        return len(self.frames)
    
    def clear(self):
        """Clear all frames"""
        self.frames = []
        return self
