"""
character_asset_generator.py - Character sprite asset management
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class CharacterAssetGenerator:
    def __init__(self, assets_dir: Path):
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.characters_dir = self.assets_dir / "characters"
        self.characters_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_character_assets(self, character_profile: Dict, job_id: str) -> Dict:
        """Generate character sprite set from profile"""
        try:
            char_name = character_profile.get("name", "character").lower()
            char_dir = self.characters_dir / job_id / char_name
            char_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"[{job_id}] Generating assets for {char_name}")
            
            assets = self._create_sprites(char_dir, character_profile)
            metadata = self._create_metadata(character_profile, assets)
            
            with open(char_dir / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return assets
        except Exception as e:
            logger.error(f"[{job_id}] Failed: {str(e)}")
            raise
    
    def _create_sprites(self, char_dir: Path, profile: Dict) -> Dict[str, Path]:
        """Create sprite placeholder files"""
        assets = {}
        
        try:
            from PIL import Image, ImageDraw
            color = self._hex_to_rgb(profile.get("colors", ["#4169E1"])[0])
            
            for sprite_type in ["idle", "talking_01", "talking_02", "talking_03", "talking_04", "talking_05"]:
                filepath = char_dir / f"{sprite_type}.png"
                img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
                draw = ImageDraw.Draw(img)
                draw.ellipse([(64, 30), (192, 130)], fill=color + (255,))
                draw.rectangle([(80, 130), (176, 220)], fill=color + (200,))
                img.save(filepath)
                assets[sprite_type] = filepath
        except:
            # Fallback: create text placeholders
            for sprite_type in ["idle", "talking_01", "talking_02", "talking_03", "talking_04", "talking_05"]:
                filepath = char_dir / f"{sprite_type}.txt"
                filepath.write_text(sprite_type)
                assets[sprite_type] = filepath
        
        return assets
    
    def _create_metadata(self, profile: Dict, assets: Dict) -> Dict:
        """Create character metadata"""
        return {
            "name": profile.get("name"),
            "gender": profile.get("gender", "neutral"),
            "voice_type": profile.get("voice_type", "neutral"),
            "colors": profile.get("colors", ["#4169E1"]),
            "sprites": {k: str(v) for k, v in assets.items()},
            "talking_frames": 6,
            "expressions": ["idle", "happy", "sad", "angry", "neutral"]
        }
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
