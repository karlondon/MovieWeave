"""
story_analyzer.py - Extract screenplay data from story text
"""
import logging
import re
from typing import List, Dict

logger = logging.getLogger(__name__)

class StoryAnalyzer:
    def analyze_story(self, story_text: str, job_id: str) -> dict:
        """Convert story into screenplay with characters and scenes"""
        logger.info(f"[{job_id}] Analyzing {len(story_text)} chars")
        
        return {
            "title": self._extract_title(story_text),
            "genre": self._detect_genre(story_text),
            "characters": self._extract_characters(story_text),
            "scenes": self._extract_scenes(story_text),
            "total_duration_seconds": 180.0,
            "animation_style": "2d",
            "fps": 24
        }
    
    def _extract_title(self, text: str) -> str:
        lines = text.split('\n')
        return lines[0].strip()[:100] if lines else "Untitled"
    
    def _detect_genre(self, text: str) -> str:
        text_lower = text.lower()
        if any(w in text_lower for w in ["magic", "dragon", "wizard"]):
            return "fantasy"
        if any(w in text_lower for w in ["adventure", "quest"]):
            return "adventure"
        return "general"
    
    def _extract_characters(self, text: str) -> List[dict]:
        """Extract character names from text"""
        patterns = [r'([A-Z][a-z]+)\s+(?:was|is)', r'(?:Meet|There was)\s+([A-Z][a-z]+)']
        names = set()
        
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1)
                if len(name) > 2:
                    names.add(name)
        
        names = names or {"Character"}
        return [{"name": n, "description": "Character", "voice": "neutral"} for n in list(names)[:5]]
    
    def _extract_scenes(self, text: str) -> List[dict]:
        """Extract scenes from text"""
        chunks = re.split(r'(?<=[.!?])\s+', text)[:10]
        scenes = []
        
        for idx, chunk in enumerate(chunks):
            if len(chunk.strip()) < 20:
                continue
            scenes.append({
                "id": idx,
                "title": f"Scene {idx + 1}",
                "description": chunk[:150],
                "setting": "Location",
                "duration_seconds": 30.0,
                "characters": ["Character"]
            })
        
        return scenes if scenes else [{"id": 0, "title": "Scene 1", "description": text[:150], 
                                      "setting": "Location", "duration_seconds": 60.0, "characters": ["Character"]}]
