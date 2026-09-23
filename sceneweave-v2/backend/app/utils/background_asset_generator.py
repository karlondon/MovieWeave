"""
background_asset_generator.py - Generate scene background assets
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class BackgroundAssetGenerator:
    """Generate background assets for scenes"""
    
    def __init__(self, assets_dir: Path):
        self.assets_dir = Path(assets_dir)
        self.backgrounds_dir = self.assets_dir / "backgrounds"
        self.backgrounds_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_background(self, scene_desc: Dict, job_id: str, scene_id: int) -> Dict:
        """Generate background for a scene"""
        try:
            logger.info(f"[{job_id}] Scene {scene_id} background")
            
            bg_dir = self.backgrounds_dir / job_id
            bg_dir.mkdir(parents=True, exist_ok=True)
            bg_path = bg_dir / f"scene_{scene_id}_bg.png"
            
            self._create_background_image(
                bg_path,
                scene_desc.get("environment", "generic"),
                scene_desc.get("mood", "neutral"),
                scene_desc.get("colors", ["#4169E1"])
            )
            
            metadata = {
                "scene_id": scene_id,
                "setting": scene_desc.get("setting", "Unknown"),
                "environment": scene_desc.get("environment", "generic"),
                "mood": scene_desc.get("mood", "neutral"),
                "colors": scene_desc.get("colors", []),
                "path": str(bg_path)
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"[{job_id}] Background failed: {str(e)}")
            raise
    
    def _create_background_image(self, filepath: Path, environment: str, mood: str, colors: List[str]):
        """Create background image"""
        try:
            from PIL import Image, ImageDraw
            
            bg = Image.new('RGB', (1920, 1080), (255, 255, 255))
            draw = ImageDraw.Draw(bg)
            
            base_color = self._get_env_color(environment)
            mood_color = self._get_mood_color(mood)
            
            # Gradient background
            for y in range(1080):
                ratio = y / 1080
                r = int(base_color[0] * (1 - ratio) + mood_color[0] * ratio)
                g = int(base_color[1] * (1 - ratio) + mood_color[1] * ratio)
                b = int(base_color[2] * (1 - ratio) + mood_color[2] * ratio)
                draw.line([(0, y), (1920, y)], fill=(r, g, b))
            
            bg.save(filepath)
            
        except ImportError:
            # Fallback: text file
            filepath = filepath.with_suffix('.txt')
            filepath.write_text(f"{environment}_{mood}")
    
    def _get_env_color(self, env: str) -> tuple:
        """Base color for environment"""
        colors = {
            "nature": (34, 139, 34),
            "fantasy": (70, 70, 130),
            "urban": (128, 128, 128),
            "coastal": (135, 206, 235),
            "sci-fi": (25, 25, 112),
            "interior": (210, 180, 140),
            "generic": (100, 150, 200)
        }
        return colors.get(env.lower(), colors["generic"])
    
    def _get_mood_color(self, mood: str) -> tuple:
        """Overlay color for mood"""
        moods = {
            "happy": (255, 255, 100),
            "sad": (100, 100, 150),
            "tense": (200, 50, 50),
            "mysterious": (80, 40, 120),
            "peaceful": (150, 200, 150),
            "neutral": (150, 150, 150)
        }
        return moods.get(mood.lower(), moods["neutral"])
