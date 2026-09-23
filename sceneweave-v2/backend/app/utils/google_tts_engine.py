"""
google_tts_engine.py - Google Cloud Text-to-Speech integration
Converts dialogue text to natural-sounding audio
"""

import logging
import os
from typing import Optional
import requests
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class GoogleTTSEngine:
    """Google Cloud Text-to-Speech engine"""
    
    def __init__(self, api_key: str):
        """Initialize with Google Cloud API key"""
        self.api_key = api_key
        self.base_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
        self.voice_mapping = {
            "male": "en-US-Neural2-C",
            "female": "en-US-Neural2-E",
            "neutral": "en-US-Neural2-A"
        }
    
    def synthesize(self, text: str, voice_type: str = "neutral", 
                   emotion: str = "neutral", output_path: str = None) -> str:
        """
        Synthesize speech from text using Google Cloud TTS
        
        Args:
            text: Text to convert to speech
            voice_type: male, female, or neutral
            emotion: emotion hint (not directly used by Google, affects speaking style)
            output_path: where to save the WAV file
        
        Returns:
            Path to generated audio file
        """
        try:
            voice = self.voice_mapping.get(voice_type, self.voice_mapping["neutral"])
            
            # Map emotion to speaking rate and pitch
            speaking_rate = 1.0
            pitch = 0.0
            
            if emotion == "excited":
                speaking_rate = 1.2
                pitch = 3.0
            elif emotion == "sad":
                speaking_rate = 0.8
                pitch = -2.0
            elif emotion == "angry":
                speaking_rate = 1.1
                pitch = 2.0
            elif emotion == "scared":
                speaking_rate = 1.15
                pitch = 1.0
            
            payload = {
                "input": {"text": text},
                "voice": {
                    "languageCode": "en-US",
                    "name": voice
                },
                "audioConfig": {
                    "audioEncoding": "LINEAR16",
                    "speakingRate": speaking_rate,
                    "pitch": pitch
                }
            }
            
            logger.info(f"Synthesizing: {text[:50]}... ({voice_type}/{emotion})")
            
            response = requests.post(
                self.base_url,
                params={"key": self.api_key},
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                error = response.json().get("error", {})
                raise Exception(f"Google TTS error: {error.get('message', 'Unknown error')}")
            
            # Extract audio content
            audio_content = response.json().get("audioContent")
            if not audio_content:
                raise Exception("No audio content in response")
            
            # Decode and save
            import base64
            audio_bytes = base64.b64decode(audio_content)
            
            if output_path is None:
                output_path = f"/tmp/audio_{os.urandom(4).hex()}.wav"
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            
            logger.info(f"Audio saved: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"TTS synthesis failed: {str(e)}")
            raise


def create_tts_engine(api_key: str) -> GoogleTTSEngine:
    """Factory function to create TTS engine"""
    return GoogleTTSEngine(api_key)
