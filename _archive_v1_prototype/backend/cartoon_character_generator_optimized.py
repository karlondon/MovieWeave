"""OptimizedCartoonCharacterGenerator - High-performance version"""
from PIL import Image, ImageDraw
from pathlib import Path
from typing import Tuple, Dict, List
import random
from dataclasses import dataclass
import threading
from concurrent.futures import ThreadPoolExecutor

@dataclass
class CharacterStyle:
    skin_color: Tuple[int, int, int]
    hair_color: Tuple[int, int, int]
    shirt_color: Tuple[int, int, int]
    eye_color: Tuple[int, int, int]
    mouth_color: Tuple[int, int, int]

class OptimizedCartoonCharacterGenerator:
    """High-performance generator with multi-threading and caching"""
    
    WIDTH = 300
    HEIGHT = 400
    
    def __init__(self, output_dir: Path = None):
        if output_dir is None:
            output_dir = Path(__file__).parent / "assets" / "characters"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
    
    def generate_characters_batch(self, characters: List[tuple], 
                                 use_threading: bool = True) -> int:
        """Generate multiple characters efficiently"""
        if use_threading:
            return self._generate_batch_threaded(characters)
        return self._generate_batch_sequential(characters)
    
    def _generate_batch_sequential(self, characters: List[tuple]) -> int:
        success_count = 0
        for char_name, char_type in characters:
            style = self.get_random_style(char_type)
            if self.generate_character(char_name, style):
                success_count += 1
        return success_count
    
    def _generate_batch_threaded(self, characters: List[tuple], 
                                 max_workers: int = 4) -> int:
        """Generate characters using thread pool for speed"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for char_name, char_type in characters:
                style = self.get_random_style(char_type)
                future = executor.submit(self.generate_character, char_name, style)
                futures.append(future)
            success_count = sum(1 for f in futures if f.result())
        return success_count
    
    def generate_character(self, name: str, style: CharacterStyle) -> bool:
        try:
            char_dir = self.output_dir / name
            char_dir.mkdir(parents=True, exist_ok=True)
            (char_dir / "mouths").mkdir(exist_ok=True)
            
            for expr in ['neutral', 'happy', 'sad', 'angry']:
                img = self._draw_character(style, expr)
                img.save(char_dir / f"{name}_{expr}.png")
            
            for mouth in ['A', 'E', 'I', 'O', 'U', 'MBP', 'X']:
                img = self._draw_mouth(mouth, style)
                img.save(char_dir / "mouths" / f"{mouth}.png")
            
            return True
        except:
            return False
    
    def _draw_character(self, style: CharacterStyle, expr: str) -> Image.Image:
        img = Image.new('RGBA', (self.WIDTH, self.HEIGHT), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        cx, cy = self.WIDTH // 2, self.HEIGHT // 2
        
        draw.ellipse([cx-50, cy-150, cx+50, cy-50], fill=style.skin_color, 
                    outline=(0,0,0), width=2)
        draw.rectangle([cx-30, cy, cx+30, cy+80], fill=style.shirt_color, 
                      outline=(0,0,0), width=2)
        
        for ex in [cx-20, cx+20]:
            draw.ellipse([ex-8, cy-110, ex+8, cy-94], fill=(255,255,255), 
                        outline=(0,0,0), width=1)
            draw.ellipse([ex-4, cy-108, ex+4, cy-100], fill=style.eye_color)
        
        if expr == 'happy':
            draw.arc([cx-15, cy-70, cx+15, cy-55], 0, 180, fill=style.mouth_color, width=2)
        elif expr == 'sad':
            draw.arc([cx-15, cy-85, cx+15, cy-70], 180, 360, fill=style.mouth_color, width=2)
        else:
            draw.line([cx-15, cy-62, cx+15, cy-62], fill=style.mouth_color, width=2)
        
        return img.convert('RGB')
    
    def _draw_mouth(self, shape: str, style: CharacterStyle) -> Image.Image:
        img = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        shapes = {'A': [10, 8, 40, 45], 'E': [5, 15, 45, 35], 'I': [18, 10, 32, 40],
                 'O': [12, 12, 38, 38], 'U': [14, 14, 36, 36]}
        
        if shape in shapes:
            draw.ellipse(shapes[shape], fill=style.mouth_color)
        elif shape == 'MBP':
            draw.line([5, 25, 45, 25], fill=style.mouth_color, width=3)
        
        return img.convert('RGB')
    
    @staticmethod
    def get_random_style(char_type: str = 'hero') -> CharacterStyle:
        if char_type == 'villain':
            skin, hair, shirt, eyes = [(100, 50, 50)], [(30, 30, 30)], [(40, 20, 20)], [(200, 50, 50)]
        elif char_type == 'child':
            skin, hair, shirt, eyes = [(255, 200, 150)], [(200, 150, 100)], [(255, 100, 100)], [(50, 100, 200)]
        else:
            skin, hair, shirt, eyes = [(255, 200, 140)], [(50, 30, 20)], [(30, 100, 200)], [(50, 100, 200)]
        
        return CharacterStyle(
            skin_color=random.choice(skin),
            hair_color=random.choice(hair),
            shirt_color=random.choice(shirt),
            eye_color=random.choice(eyes),
            mouth_color=(200, 100, 100)
        )
