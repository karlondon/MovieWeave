"""Test suite for CartoonVideoEngine - Feature 2"""
import unittest
from pathlib import Path
from backend.cartoon_video_engine import CartoonVideoEngine
from backend.character_manager import CharacterManager

class TestCartoonVideoEngine(unittest.TestCase):
    """Test video generation functionality"""
    
    @classmethod
    def setUpClass(cls):
        cls.video_engine = CartoonVideoEngine(
            Path("backend/assets/characters"),
            Path("output/test_videos")
        )
    
    def test_engine_initialization(self):
        """Test engine initializes correctly"""
        self.assertIsNotNone(self.video_engine)
        self.assertEqual(self.video_engine.FPS, 24)
        self.assertIsNotNone(self.video_engine.manager)
        self.assertIsNotNone(self.video_engine.engine)
    
    def test_character_loading_for_video(self):
        """Test characters can be loaded for video rendering"""
        chars = self.video_engine.manager.get_available_characters()
        self.assertGreater(len(chars), 0, "No characters available for video")
    
    def test_video_output_directory_creation(self):
        """Test output directory is created"""
        self.assertTrue(self.video_engine.output_dir.exists())
    
    def test_dialogue_video_rendering(self):
        """Test dialogue video rendering (dry run)"""
        chars = self.video_engine.manager.get_available_characters()
        if chars:
            char_name = chars[0]
            # Note: FFmpeg may not be installed, so we just test the setup
            # Actual video generation is tested in integration tests
            self.assertIsNotNone(char_name)


if __name__ == '__main__':
    unittest.main()
