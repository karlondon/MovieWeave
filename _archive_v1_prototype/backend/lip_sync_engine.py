"""LipSyncEngine - Extract mouth shapes from audio for lip-sync"""
from pathlib import Path
from typing import List, Dict
import logging
import json
import subprocess

logger = logging.getLogger(__name__)

class LipSyncEvent:
    """Represents a mouth shape at a specific time"""
    def __init__(self, time: float, mouth_shape: str, phoneme: str = ""):
        self.time = time
        self.mouth_shape = mouth_shape
        self.phoneme = phoneme
    
    def to_dict(self) -> Dict:
        return {'time': self.time, 'mouth_shape': self.mouth_shape, 'phoneme': self.phoneme}

class LipSyncEngine:
    """Extracts mouth shapes from audio"""
    
    PHONEME_TO_MOUTH = {
        'A': 'A', 'E': 'E', 'I': 'I', 'O': 'O', 'U': 'U',
        'M': 'MBP', 'B': 'MBP', 'P': 'MBP',
        'rest': 'X', 'silence': 'X',
    }
    
    def __init__(self, audio_path: Path = None):
        self.audio_path = Path(audio_path) if audio_path else None
        self.events: List[LipSyncEvent] = []
    
    def load_audio(self, audio_path: Path) -> bool:
        """Load audio file"""
        audio_path = Path(audio_path)
        if not audio_path.exists():
            logger.error(f"Audio file not found: {audio_path}")
            return False
        self.audio_path = audio_path
        logger.info(f"Loaded audio: {audio_path}")
        return True
    
    def extract_mouth_shapes(self) -> List[LipSyncEvent]:
        """Extract mouth shapes from audio"""
        if not self.audio_path:
            logger.error("No audio file loaded")
            return []
        
        try:
            events = self._extract_with_rhubarb()
            if events:
                self.events = events
                return events
        except:
            pass
        
        logger.info("Using fallback mouth shape extraction")
        return self._extract_fallback()
    
    def _extract_with_rhubarb(self) -> List[LipSyncEvent]:
        """Extract using Rhubarb Lip Sync tool"""
        try:
            result = subprocess.run(
                ['rhubarb', '-f', 'json', str(self.audio_path)],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode != 0:
                return []
            
            data = json.loads(result.stdout)
            events = []
            
            for mouth_cue in data.get('mouthCues', []):
                time = mouth_cue['start']
                phoneme = mouth_cue.get('value', 'X')
                mouth_shape = self.PHONEME_TO_MOUTH.get(phoneme, 'X')
                events.append(LipSyncEvent(time, mouth_shape, phoneme))
            
            logger.info(f"Extracted {len(events)} mouth shapes")
            return events
        except:
            return []
    
    def _extract_fallback(self) -> List[LipSyncEvent]:
        """Fallback: generate default mouth sequence"""
        mouth_sequence = ['A', 'E', 'I', 'O', 'U', 'MBP', 'X']
        events = []
        time = 0.0
        i = 0
        while time < 5.0:
            mouth_shape = mouth_sequence[i % len(mouth_sequence)]
            events.append(LipSyncEvent(time, mouth_shape))
            time += 0.1
            i += 1
        logger.info(f"Generated {len(events)} fallback mouth shapes")
        return events
    
    def get_mouth_at_time(self, time: float) -> str:
        """Get mouth shape at specific time"""
        if not self.events:
            return 'X'
        closest = min(self.events, key=lambda e: abs(e.time - time))
        return closest.mouth_shape
    
    def get_events_in_range(self, start_time: float, end_time: float) -> List[LipSyncEvent]:
        """Get mouth events in time range"""
        return [e for e in self.events if start_time <= e.time <= end_time]
    
    def export_to_json(self, output_path: Path) -> bool:
        """Export mouth shapes to JSON"""
        try:
            data = {
                'audio_file': str(self.audio_path),
                'total_events': len(self.events),
                'events': [e.to_dict() for e in self.events]
            }
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Exported lip-sync data to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False
    
    def __repr__(self) -> str:
        return f"LipSyncEngine(audio={self.audio_path}, events={len(self.events)})"
