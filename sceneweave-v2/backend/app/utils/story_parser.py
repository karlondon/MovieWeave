"""
story_parser.py - Extract characters, scenes, and dialogue from narrative text
Professional story parsing for video generation
"""

import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import re

logger = logging.getLogger(__name__)

@dataclass
class Character:
    """Character definition"""
    name: str
    description: str
    age: str
    gender: str
    voice_type: str
    emotion_default: str = "neutral"

@dataclass
class DialogueLine:
    """Single line of dialogue"""
    character: str
    text: str
    emotion: str
    duration_seconds: float
    action: str = ""

@dataclass
class Scene:
    """Scene definition"""
    id: int
    name: str
    description: str
    background: str
    characters_present: List[str]
    dialogue: List[DialogueLine]
    duration_seconds: float
    visual_style: str = "cinematic animation"

@dataclass
class Screenplay:
    """Complete screenplay structure"""
    title: str
    description: str
    characters: List[Character]
    scenes: List[Scene]
    total_duration_seconds: float
    language: str = "English"
    rating: str = "G"
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "characters": [asdict(c) for c in self.characters],
            "scenes": [asdict(s) for s in self.scenes],
            "total_duration_seconds": self.total_duration_seconds,
            "language": self.language,
            "rating": self.rating
        }
