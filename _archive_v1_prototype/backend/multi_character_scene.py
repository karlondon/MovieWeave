"""
Feature 4: Multi-Character Scene Rendering
Render scenes with multiple characters in dialogue
"""

from pathlib import Path
from PIL import Image
from datetime import datetime
from backend.character_manager import CharacterManager
from backend.cartoon_video_engine import CartoonVideoEngine


class MultiCharacterScene:
    """Render scenes with multiple characters"""
    
    def __init__(self):
        self.video_engine = CartoonVideoEngine()
        self.character_manager = CharacterManager(Path('backend/assets/characters'))
    
    def create_dialogue_scene(self, characters_data: list, duration: float = 5.0,
                             audio_file: Path = None) -> Path:
        """
        Create scene with multiple characters in dialogue
        
        Args:
            characters_data: List of character configs
                [{
                    'name': 'hero_001',
                    'expression': 'happy',
                    'position': 'left',  # left, center, right
                    'start_time': 0.0,
                    'end_time': 5.0
                }, ...]
            duration: Total scene duration
            audio_file: Optional audio for lip-sync
            
        Returns:
            Path to generated MP4 file
        """
        try:
            # Load characters
            characters = {}
            for char_data in characters_data:
                name = char_data['name']
                char = self.character_manager.load_character(name)
                if char:
                    characters[name] = char
            
            if not characters:
                raise ValueError("No valid characters provided")
            
            # Generate scene frames
            output_dir = Path('output/scenes') / f"scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            frame_count = int(duration * 24)
            
            for frame_num in range(frame_count):
                time = frame_num / 24.0
                composite_frame = self._composite_characters(characters, characters_data, time)
                composite_frame.save(output_dir / f"frame_{frame_num:06d}.png")
            
            # Encode to video
            output_video = Path('output/videos') / f"scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            success = self.video_engine._encode_video(output_dir, output_video, audio_file)
            
            return output_video if success else None
            
        except Exception as e:
            raise Exception(f"Scene creation failed: {e}")
    
    def _composite_characters(self, characters: dict, scene_data: list, time: float):
        """Composite multiple character frames into one scene"""
        canvas = Image.new('RGB', (800, 400), (255, 255, 255))
        positions = {'left': 50, 'center': 300, 'right': 550}
        
        for char_data in scene_data:
            if time < char_data['start_time'] or time > char_data['end_time']:
                continue
            
            name = char_data['name']
            if name not in characters:
                continue
            
            char = characters[name]
            frame = char.render_frame(char_data['expression'], 'X')
            x = positions.get(char_data['position'], 300)
            canvas.paste(frame, (x, 50))
        
        return canvas
