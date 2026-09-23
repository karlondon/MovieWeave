"""
llm_processor.py - LLM integration for screenplay generation
Supports both Ollama (local) and Groq (cloud API)
"""
import json
import logging
import os
import re
from typing import Optional
import requests
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class ScriptGenerationError(Exception):
    """Error during script generation"""
    pass

def repair_json(json_str: str) -> str:
    """
    Attempt to repair common JSON formatting issues from LLM responses
    """
    try:
        # First try parsing as-is
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # Clean up common LLM JSON issues
    
    # Remove trailing commas before closing braces/brackets
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    
    # Fix unescaped quotes in string values
    # This is tricky - look for quotes that aren't properly escaped
    json_str = re.sub(r'(?<!\\)"(?=\w)', r'\\"', json_str)
    
    # Fix newlines within JSON strings (common issue)
    # Replace actual newlines with \n
    json_str = json_str.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    # Remove trailing commas in arrays
    json_str = re.sub(r',(\s*[\]}])', r'\1', json_str)
    
    # Fix double commas
    json_str = re.sub(r',,+', ',', json_str)
    
    # Ensure all string values are properly quoted
    # This is a last-resort fix for common patterns
    json_str = re.sub(r': (\w+)([,\}])', r': "\1"\2', json_str)
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON repair failed: {str(e)}")
        logger.error(f"Attempted to repair: {json_str[:300]}...")
        raise


class GroqScriptGenerator:
    """Generate structured screenplay JSON from text using Groq API"""
    
    def __init__(self, api_key: str = None, model: str = "openai/gpt-oss-120b"):
        """
        Initialize Groq connection
        
        Args:
            api_key: Groq API key (if None, reads from GROQ_API_KEY env var)
            model: Model name (default: openai/gpt-oss-120b - recommended for screenplay generation)
        """
        # Try multiple ways to get the API key
        self.api_key = api_key
        logger.info(f"[Groq Init] Step 1 - Direct param: {bool(self.api_key)}")
        
        if not self.api_key:
            # Try from environment variable
            self.api_key = os.getenv("GROQ_API_KEY")
            logger.info(f"[Groq Init] Step 2 - Env var: {bool(self.api_key)}")
        
        if not self.api_key:
            # Try from config settings
            try:
                from app.config import settings
                self.api_key = settings.GROQ_API_KEY
                logger.info(f"[Groq Init] Step 3 - Config: {bool(self.api_key)}")
            except Exception as e:
                logger.warning(f"[Groq Init] Step 3 - Config failed: {e}")
        
        logger.info(f"[Groq Init] Final status: api_key={'SET' if self.api_key else 'MISSING'}, len={len(self.api_key) if self.api_key else 0}")
        
        if not self.api_key:
            raise ScriptGenerationError("GROQ_API_KEY not found in environment variables. Please set GROQ_API_KEY in your .env file")
        
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        logger.info(f"[Groq Init] ✅ Groq initialized with model: {self.model}")
    def generate_script(self, text: str, job_id: str) -> dict:
        """
        Generate structured screenplay from input text
        
        Args:
            text: Input narrative text
            job_id: Job ID for tracking
            
        Returns:
            Structured screenplay dict with scenes, characters, dialogue, etc.
        """
        try:
            logger.info(f"[{job_id}] Starting script generation from {len(text)} chars")
            
            # Create detailed prompt for screenplay generation
            prompt = self._create_prompt(text)
            
            # Call Groq API
            logger.info(f"[{job_id}] Calling Groq API with model: {self.model}")
            response = self._call_groq(prompt)
            
            if not response:
                raise ScriptGenerationError("Empty response from Groq")
            
            # Parse JSON from response
            script = self._parse_response(response, job_id)
            
            logger.info(f"[{job_id}] Generated screenplay with {len(script.get('scenes', []))} scenes")
            return script
            
        except Exception as e:
            logger.error(f"[{job_id}] Script generation failed: {str(e)}")
            raise ScriptGenerationError(f"Failed to generate script: {str(e)}")
    
    def _create_prompt(self, text: str) -> str:
        """Create detailed prompt for screenplay generation"""
        return f"""You are a professional screenwriter. Convert the following narrative text into a structured screenplay JSON.

IMPORTANT: Respond ONLY with valid JSON, no other text.

The JSON must have this exact structure:
{{
  "title": "string",
  "description": "string",
  "scenes": [
    {{
      "id": 1,
      "name": "string",
      "description": "string",
      "background": "string (noun describing setting)",
      "duration_seconds": number,
      "characters": ["name1", "name2"],
      "dialogue": [
        {{
          "character": "string",
          "text": "string",
          "emotion": "string (happy, sad, angry, scared, neutral, excited)",
          "action": "string (optional action description)"
        }}
      ]
    }}
  ],
  "characters": [
    {{
      "name": "string",
      "description": "string",
      "age": "string",
      "voice_type": "string (male, female, neutral)"
    }}
  ],
  "metadata": {{
    "total_duration_seconds": number,
    "language": "string",
    "rating": "string"
  }}
}}

Narrative text to convert:
{text}

Requirements:
- Each scene should be 5-15 seconds duration
- Emotions should be one of: happy, sad, angry, scared, neutral, excited
- Backgrounds should be single noun descriptions (e.g., "forest", "office", "beach")
- Include meaningful dialogue with emotions
- Ensure scenes flow logically
- Total duration should be reasonable (60-300 seconds)

Generate the screenplay JSON now:"""
    
    def _call_groq(self, prompt: str) -> str:
        """Call Groq API and get response"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
            }
            
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=60  # 60 second timeout
            )
            response.raise_for_status()
            
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                raise ScriptGenerationError("No content in Groq response")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Groq API error: {str(e)}")
            raise ScriptGenerationError(f"Groq API error: {str(e)}")
    
    def _parse_response(self, response: str, job_id: str) -> dict:
        """Parse JSON from Ollama response"""
        try:
            # Extract JSON from response (may have extra text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ScriptGenerationError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            
            # Try to repair and parse JSON
            try:
                script = repair_json(json_str)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {str(e)}")
                logger.error(f"Response preview: {response[:500]}")
                raise ScriptGenerationError(f"Failed to parse screenplay JSON: {str(e)}")
            
            # Validate structure
            if "scenes" not in script or "characters" not in script:
                raise ScriptGenerationError("Invalid screenplay structure")
            
            # Add metadata
            script["generated_at"] = datetime.utcnow().isoformat()
            script["job_id"] = job_id
            
            return script
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Response preview: {response[:500]}")
            raise ScriptGenerationError(f"Failed to parse screenplay JSON: {str(e)}")

def create_generator(api_key: str = None, model: str = "openai/gpt-oss-120b"):
    """Factory function to create script generator (uses Groq with openai/gpt-oss-120b model)"""
    return GroqScriptGenerator(api_key, model)
