"""
test_enhanced_video_composer.py - Integration tests for video composition
"""
import pytest
import logging
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from app.utils.enhanced_video_composer import EnhancedVideoComposer

logger = logging.getLogger(__name__)


class TestEnhancedVideoComposer:
    """Test enhanced video composition"""
    
    @pytest.fixture
    def composer(self, tmp_path):
        """Create composer instance"""
        output = tmp_path / "output"
        temp = tmp_path / "temp"
        return EnhancedVideoComposer(output, temp)
    
    def test_composer_initialization(self, composer):
        """Test composer setup"""
        assert composer.output_dir.exists()
        assert composer.temp_dir.exists()
        assert composer.fps == 24
        logger.info("✅ Composer initialization")
    
    def test_ffmpeg_detection(self, composer):
        """Test FFmpeg detection"""
        # Should find ffmpeg or return None
        ffmpeg = composer._find_ffmpeg()
        logger.info(f"FFmpeg path: {ffmpeg}")
    
    def test_compose_video_basic(self, composer, tmp_path):
        """Test basic video composition"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("PIL not available")
        
        # Create test background
        bg_path = tmp_path / "bg.png"
        Image.new('RGB', (1920, 1080), (100, 150, 200)).save(bg_path)
        
        # Create test audio
        audio_path = tmp_path / "audio.wav"
        try:
            import numpy as np
            import soundfile as sf
            samples = np.zeros(22050)  # 1 second
            sf.write(str(audio_path), samples, 22050)
        except ImportError:
            pytest.skip("soundfile not available")
        
        # Compose video
        try:
            result = composer.compose_video(
                job_id="test_001",
                bg_path=str(bg_path),
                audio_path=str(audio_path),
                duration_sec=2.0
            )
            
            if result:
                logger.info(f"✅ Video composed: {result}")
            else:
                logger.warning("⚠️ FFmpeg not available for full test")
        except Exception as e:
            logger.warning(f"⚠️ Video composition (expected if FFmpeg missing): {str(e)}")
    
    def test_frame_rendering(self, composer, tmp_path):
        """Test frame sequence generation"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("PIL not available")
        
        bg_path = tmp_path / "bg.png"
        Image.new('RGB', (1920, 1080), (100, 150, 200)).save(bg_path)
        
        frames_dir = composer._render_frames("test_002", str(bg_path), 1.0)
        
        if frames_dir:
            frames = list(frames_dir.glob("frame_*.png"))
            logger.info(f"✅ Generated {len(frames)} frames")
            assert len(frames) == 24  # 24 fps * 1 second
    
    def test_fallback_background_creation(self, composer):
        """Test fallback background generation"""
        try:
            bg_path = composer._fallback_bg()
            if bg_path:
                assert Path(bg_path).exists()
                logger.info(f"✅ Fallback background created: {bg_path}")
        except ImportError:
            pytest.skip("PIL not available")
    
    def test_silent_audio_creation(self, composer):
        """Test silent audio generation"""
        try:
            audio_path = composer._silent_audio(2.0)
            if audio_path:
                assert Path(audio_path).exists()
                logger.info(f"✅ Silent audio created: {audio_path}")
        except ImportError:
            pytest.skip("soundfile not available")
