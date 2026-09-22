"""
storyboard_engine.py - AI-Powered Storyboarding Engine
Converts stories into detailed storyboards with character info and visual descriptions
"""
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class StoryboardEngine:
    """Analyzes stories and creates detailed storyboards for character animation"""

    def __init__(self, llm_generator=None):
        self.llm = llm_generator

    def create_storyboard(self, story_text: str, job_id: str) -> Dict[str, Any]:
        """Create a detailed storyboard from story text"""
        try:
            logger.info(f"[{job_id}] Creating storyboard from {len(story_text)} chars")

            # Extract story structure (characters, plot, tone)
            structure = self._extract_story_structure(story_text, job_id)

            # Generate detailed scenes with visual descriptions
            scenes = self._generate_scenes(story_text, structure, job_id)

            storyboard = {
                "title": structure.get("title", "Untitled Story"),
                "summary": structure.get("summary", ""),
                "genre": structure.get("genre", "adventure"),
                "tone": structure.get("tone", "lighthearted"),
                "setting": structure.get("setting", "fantasy world"),
                "characters": structure.get("characters", []),
                "scenes": scenes,
                "total_duration_seconds": sum(s.get("duration_seconds", 45) for s in scenes),
            }

            logger.info(
                f"[{job_id}] Storyboard created: {len(scenes)} scenes, "
                f"{storyboard['total_duration_seconds']}s total"
            )
            return storyboard

        except Exception as e:
            logger.error(f"[{job_id}] Storyboard generation failed: {e}", exc_info=True)
            raise

    def _extract_story_structure(
        self, story_text: str, job_id: str
    ) -> Dict[str, Any]:
        """Extract high-level story structure using LLM"""

        if not self.llm:
            return self._fallback_structure(story_text)

        prompt = f"""Analyze this story and extract its structure as JSON.
Focus on: characters, plot, tone, and setting.

Story:
{story_text[:2000]}

Respond ONLY with valid JSON (no markdown):
{{
  "title": "Story title",
  "summary": "2-3 sentence summary",

    def _generate_scenes(
        self, story_text: str, structure: Dict, job_id: str
    ) -> List[Dict]:
        """Generate detailed scene descriptions"""

        # Target: 3-5 minute video = 4-6 scenes at 45-60s each
        num_scenes = min(6, max(4, len(story_text) // 500))

        if not self.llm:
            return self._fallback_scenes(story_text, structure, num_scenes)

        prompt = f"""Break this story into {num_scenes} engaging video scenes.
Each scene: 45-60 seconds of narration. Include characters, visuals, and any dialogue.

Story:
{story_text[:1500]}

Respond ONLY with JSON array (no markdown):
[
  {{
    "id": 1,
    "title": "Scene title",
    "duration_seconds": 50,
    "location": "Setting",
    "visual_description": "What we see - colors, mood, action",
    "characters_in_scene": ["Character 1"],
    "narration": "Narrator voiceover",
    "visual_prompt": "Image generation prompt",
    "story_excerpt": "Relevant text"
  }}
]"""

        try:
            response = self.llm._call_groq(prompt)
            json_start = response.find("[")
            json_end = response.rfind("]") + 1

            if json_start == -1 or json_end == 0:
                return self._fallback_scenes(story_text, structure, num_scenes)

            scenes = json.loads(response[json_start:json_end])
            logger.info(f"[{job_id}] Generated {len(scenes)} scenes")
            return scenes

        except Exception as e:
            logger.warning(f"[{job_id}] Scene generation failed: {e}")
            return self._fallback_scenes(story_text, structure, num_scenes)

    def _fallback_structure(self, story_text: str) -> Dict:
        """Fallback structure when LLM unavailable"""
        lines = story_text.split("\n")
        title = lines[0].strip() if lines else "Untitled Story"

        return {
            "title": title,
            "summary": story_text[:200],
            "genre": "adventure",
            "tone": "lighthearted",
            "setting": "magical world",
            "characters": [
                {
                    "name": "Hero",
                    "role": "protagonist",
                    "description": "A brave adventurer",
                    "voice_type": "neutral",
                }
            ],
        }

    def _fallback_scenes(
        self, story_text: str, structure: Dict, num_scenes: int
    ) -> List[Dict]:
        """Fallback scene generation when LLM unavailable"""
        paragraphs = [p.strip() for p in story_text.split("\n\n") if p.strip()]

        if not paragraphs:
            paragraphs = [story_text]

        chunk_size = max(1, len(paragraphs) // num_scenes)
        scenes = []

        for scene_idx in range(num_scenes):
            start_idx = scene_idx * chunk_size
            end_idx = min(start_idx + chunk_size, len(paragraphs))

            scene_content = " ".join(paragraphs[start_idx:end_idx])[:400]
            characters = structure.get("characters", [])
            main_char = characters[0]["name"] if characters else "Hero"

            scenes.append(
                {
                    "id": scene_idx + 1,
                    "title": f"Scene {scene_idx + 1}",
                    "duration_seconds": 50,
                    "location": structure.get("setting", "magical place"),
                    "visual_description": "Enchanted world with magical elements",
                    "characters_in_scene": [main_char],
                    "narration": scene_content,
                    "visual_prompt": f"cartoon animation, magical fantasy, {structure.get('setting', 'forest')}",
                    "story_excerpt": scene_content,
                }
            )

        return scenes

  "genre": "fantasy/adventure/romance/mystery/sci-fi",
  "tone": "lighthearted/serious/dark/humorous",
  "setting": "Primary location",
  "characters": [
    {{
      "name": "Character name",
      "role": "protagonist/antagonist/side",
      "description": "Appearance and personality",
      "voice_type": "male/female/neutral"
    }}
  ]
}}"""

        try:
            response = self.llm._call_groq(prompt)
            structure = self.llm._parse_response(response, job_id)
            return structure
        except Exception as e:
            logger.warning(f"[{job_id}] Structure extraction failed: {e}")
            return self._fallback_structure(story_text)
