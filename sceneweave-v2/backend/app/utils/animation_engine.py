"""
animation_engine.py - Generate character animations and lip-sync
Converts dialogue to keyframes and visemes
"""
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class VisemeMapper:
    """Map text to visemes for lip-sync"""
    
    VISEME_MAP = {
        'a': 'A', 'e': 'E', 'i': 'I', 'o': 'O', 'u': 'U',
        'p': 'P', 'b': 'P', 'm': 'P',
        'f': 'F', 'v': 'F',
        't': 'T', 'd': 'T', 'n': 'T',
        's': 'S', 'z': 'S',
        'th': 'TH', 'ch': 'CH', 'sh': 'SH', 'j': 'CH',
    }
    
    @staticmethod
    def text_to_visemes(text: str, duration_ms: int) -> List[Dict]:
        """Convert text to viseme keyframes"""
        text_lower = text.lower()
        visemes = []
        char_duration = max(50, duration_ms // max(len(text), 1))
        
        for idx, char in enumerate(text_lower):
            time_ms = idx * char_duration
            viseme = VisemeMapper.VISEME_MAP.get(char, 'neutral')
            visemes.append({"time_ms": time_ms, "viseme": viseme})
        
        return visemes


class AnimationEngine:
    """Generate character animations from screenplay"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_scene_animations(self, scene: Dict, job_id: str, scene_id: int) -> Dict:
        """Generate all animations for a scene"""
        try:
            logger.info(f"[{job_id}] Generating animations for scene {scene_id}")
            
            animations = {
                "scene_id": scene_id,
                "duration_ms": int(scene.get("duration_seconds", 30) * 1000),
                "characters": {}
            }
            
            for char_idx, char_name in enumerate(scene.get("characters", [])):
                char_dialogue = [d for d in scene.get("dialogue", []) 
                                if d.get("character") == char_name]
                
                animations["characters"][char_name] = {
                    "position_keyframes": self._position_keyframes(scene, char_idx, char_dialogue),
                    "expression_keyframes": self._expression_keyframes(char_dialogue),
                    "lipsync_keyframes": self._lipsync_keyframes(char_dialogue)
                }
            
            return animations
            
        except Exception as e:
            logger.error(f"[{job_id}] Animation failed: {str(e)}")
            raise
    
    def _position_keyframes(self, scene: Dict, char_idx: int, dialogue: List[Dict]) -> List[Dict]:
        """Generate character position keyframes"""
        x_positions = [400, 960, 1520]
        start_x = x_positions[char_idx % len(x_positions)]
        duration_ms = int(scene.get("duration_seconds", 30) * 1000)
        
        keyframes = [
            {"time_ms": 0, "x": start_x, "y": 400, "scale": 1.0},
            {"time_ms": duration_ms, "x": start_x, "y": 400, "scale": 1.0}
        ]
        
        return keyframes
    
    def _expression_keyframes(self, dialogue: List[Dict]) -> List[Dict]:
        """Generate facial expression keyframes"""
        keyframes = []
        current_time_ms = 0
        
        for line in dialogue:
            emotion = line.get("emotion", "neutral")
            duration_ms = int(line.get("duration_seconds", 2.0) * 1000)
            
            keyframes.append({"time_ms": current_time_ms, "expression": emotion})
            keyframes.append({"time_ms": current_time_ms + duration_ms, "expression": "neutral"})
            
            current_time_ms += duration_ms + 300
        
        return keyframes
    
    def _lipsync_keyframes(self, dialogue: List[Dict]) -> List[Dict]:
        """Generate lip-sync keyframes"""
        keyframes = []
        current_time_ms = 0
        
        for line in dialogue:
            text = line.get("text", "")
            duration_ms = int(line.get("duration_seconds", 2.0) * 1000)
            
            visemes = VisemeMapper.text_to_visemes(text, duration_ms)
            for v in visemes:
                v["time_ms"] += current_time_ms
                keyframes.append(v)
            
            current_time_ms += duration_ms + 300
        
        return keyframes
    
    def save_animations(self, animations: Dict, job_id: str, scene_id: int) -> Path:
        """Save animation keyframes to JSON"""
        anim_dir = self.output_dir / job_id / "animations"
        anim_dir.mkdir(parents=True, exist_ok=True)
        
        anim_file = anim_dir / f"scene_{scene_id}.json"
        with open(anim_file, 'w') as f:
            json.dump(animations, f, indent=2)
        
        return anim_file
    
    def get_animations(self, job_id: str, scene_id: int) -> Optional[Dict]:
        """Retrieve animation keyframes"""
        anim_file = self.output_dir / job_id / "animations" / f"scene_{scene_id}.json"
        
        if anim_file.exists():
            with open(anim_file, 'r') as f:
                return json.load(f)
        return None
