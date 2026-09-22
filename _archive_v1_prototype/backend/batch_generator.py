"""
Feature 4: Batch Video Generation
Generate multiple videos asynchronously with progress tracking
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json
from backend.cartoon_video_engine import CartoonVideoEngine


class BatchVideoGenerator:
    """Generate multiple videos in batch"""
    
    def __init__(self):
        self.video_engine = CartoonVideoEngine()
        self.results = []
    
    def generate_batch(self, videos_config: List[Dict], audio_file: Optional[Path] = None) -> Dict:
        """
        Generate multiple videos
        
        Args:
            videos_config: List of video configs
                [{
                    'character_name': 'hero_001',
                    'expression': 'happy',
                    'duration': 3.0
                }, ...]
            audio_file: Optional shared audio file
            
        Returns:
            {'success': True, 'total': X, 'generated': Y, 'videos': [...]}
        """
        self.results = []
        total_videos = len(videos_config)
        generated_count = 0
        
        for index, video_config in enumerate(videos_config):
            try:
                character_name = video_config.get('character_name')
                expression = video_config.get('expression', 'neutral')
                duration = video_config.get('duration', 3.0)
                
                # Generate video filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
                output_file = Path('output/videos') / f"{character_name}_{expression}_{timestamp}.mp4"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Generate video
                success = self.video_engine.render_dialogue_video(
                    character_name=character_name,
                    expression=expression,
                    duration_seconds=duration,
                    audio_file=audio_file,
                    output_file=output_file
                )
                
                if success:
                    self.results.append({
                        'character': character_name,
                        'expression': expression,
                        'file': output_file.name,
                        'duration': duration,
                        'status': 'success'
                    })
                    generated_count += 1
                else:
                    self.results.append({
                        'character': character_name,
                        'expression': expression,
                        'status': 'failed',
                        'error': 'Video generation returned false'
                    })
                
                # Progress callback
                progress = (index + 1) / total_videos * 100
                print(f"Progress: {progress:.1f}% ({index + 1}/{total_videos})")
                
            except Exception as e:
                self.results.append({
                    'character': video_config.get('character_name', 'unknown'),
                    'status': 'error',
                    'error': str(e)
                })
        
        return {
            'success': generated_count > 0,
            'total': total_videos,
            'generated': generated_count,
            'failed': total_videos - generated_count,
            'videos': self.results
        }
    
    def save_results(self, output_file: Path = None) -> Path:
        """Save batch results to JSON"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path('output/batch_results') / f"batch_{timestamp}.json"
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return output_file
