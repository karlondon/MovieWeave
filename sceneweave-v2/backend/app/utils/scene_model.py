"""
scene_model.py - Scene and dialogue data models
"""
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any

@dataclass
class DialogueLine:
    """Single line of dialogue with timing and animation sync"""
    character: str
    text: str
    emotion: str
    duration_seconds: float
    start_time_seconds: float = 0.0
    
    def to_dict(self):
        return asdict(self)

@dataclass
class SceneDescription:
    """Detailed scene with visual and narrative elements"""
    scene_id: int
    title: str
    description: str
    setting: str
    environment_type: str  # nature, fantasy, urban, coastal, sci-fi, interior
    lighting: str  # bright, dim, dramatic, warm, cool
    background_style: str  # cinematic, cartoon, watercolor, photorealistic
    characters_present: List[str]
    character_positions: Dict[str, Dict[str, Any]]
    dialogue_lines: List[DialogueLine]
    actions: List[str]
    duration_seconds: float
    mood: str  # happy, sad, tense, mysterious, peaceful
    color_palette: List[str] = field(default_factory=lambda: ["#4169E1", "#87CEEB"])
    camera_angles: List[str] = field(default_factory=lambda: ["wide", "medium", "close-up"])
    transitions: Dict[str, str] = field(default_factory=lambda: {"type": "cut"})
    
    def to_dict(self):
        data = asdict(self)
        data['dialogue_lines'] = [d.to_dict() for d in self.dialogue_lines]
        return data

@dataclass
class VisualScreenplay:
    """Complete visual screenplay with animation data"""
    title: str
    description: str
    genre: str
    characters: List  # List[CharacterProfile]
    scenes: List[SceneDescription]
    total_duration_seconds: float
    animation_style: str = "2d"
    target_fps: int = 24
    resolution: str = "1920x1080"
    aspect_ratio: str = "16:9"
    language: str = "English"
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "genre": self.genre,
            "characters": [c.to_dict() if hasattr(c, 'to_dict') else c for c in self.characters],
            "scenes": [s.to_dict() for s in self.scenes],
            "total_duration_seconds": self.total_duration_seconds,
            "animation_style": self.animation_style,
            "target_fps": self.target_fps,
            "resolution": self.resolution,
            "aspect_ratio": self.aspect_ratio,
            "language": self.language
        }
