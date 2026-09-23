"""
character_profile.py - Character data models for animation
"""
from dataclasses import dataclass, asdict, field
from typing import List

@dataclass
class CharacterProfile:
    """Detailed character profile for animation"""
    name: str
    description: str
    age: str
    gender: str
    appearance: str
    personality_traits: List[str]
    voice_type: str  # soprano, alto, baritone, tenor
    voice_speed: int = 140  # words per minute
    accent: str = "neutral"
    default_emotion: str = "neutral"
    color_palette: List[str] = field(default_factory=lambda: ["#4169E1", "#87CEEB"])
    animation_style: str = "2d"
    
    def to_dict(self):
        return asdict(self)
