"""Unit tests for Feature 1: Cartoon Character System"""
import pytest
from pathlib import Path
import tempfile
from PIL import Image

from backend.cartoon_character_generator import CartoonCharacterGenerator, CharacterStyle
from backend.cartoon_character import CartoonCharacter
from backend.character_manager import CharacterManager
from backend.lip_sync_engine import LipSyncEngine, LipSyncEvent


class TestCharacterStyle:
    """Test CharacterStyle dataclass"""
    
    def test_character_style_creation(self):
        """Test creating a character style"""
        style = CharacterStyle(
            skin_color=(255, 200, 140),
            hair_color=(50, 30, 20),
            shirt_color=(30, 100, 200),
            eye_color=(50, 100, 200),
            mouth_color=(200, 100, 100)
        )
        
        assert style.skin_color == (255, 200, 140)
        assert style.hair_color == (50, 30, 20)
        assert style.mouth_color == (200, 100, 100)
        assert style.eye_color == (50, 100, 200)


class TestCartoonCharacterGenerator:
    """Test character generation"""
    
    def test_generator_initialization(self):
        """Test generator creates output directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = CartoonCharacterGenerator(Path(tmpdir))
            assert gen.output_dir.exists()
    
    def test_get_random_style_hero(self):
        """Test hero style generation"""
        style = CartoonCharacterGenerator.get_random_style('hero')
        assert style.skin_color is not None
        assert style.hair_color is not None
        assert style.shirt_color is not None
    
    def test_get_random_style_villain(self):
        """Test villain style generation"""
        style = CartoonCharacterGenerator.get_random_style('villain')
        assert style.skin_color is not None
        assert isinstance(style.skin_color, tuple)
    
    def test_get_random_style_child(self):
        """Test child style generation"""
        style = CartoonCharacterGenerator.get_random_style('child')
        assert style.skin_color is not None
        assert isinstance(style.skin_color, tuple)
    
    def test_draw_character_neutral(self):
        """Test drawing neutral character"""
        style = CharacterStyle(
            skin_color=(255, 200, 140),
            hair_color=(50, 30, 20),
            shirt_color=(30, 100, 200),
            eye_color=(50, 100, 200),
            mouth_color=(200, 100, 100)
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = CartoonCharacterGenerator(Path(tmpdir))
            img = gen._draw_character(style, 'neutral')
            
            assert img is not None
            assert img.size == (300, 400)
    
    def test_draw_mouth_shapes(self):
        """Test drawing all mouth shapes"""
        style = CharacterStyle(
            skin_color=(255, 200, 140),
            hair_color=(50, 30, 20),
            shirt_color=(30, 100, 200),
            eye_color=(50, 100, 200),
            mouth_color=(200, 100, 100)
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = CartoonCharacterGenerator(Path(tmpdir))
            
            for mouth in ['A', 'E', 'I', 'O', 'U', 'MBP', 'X']:
                img = gen._draw_mouth(mouth, style)
                assert img is not None
                assert img.size == (50, 50)
    
    def test_generate_character_complete(self):
        """Test generating complete character"""
        style = CharacterStyle(
            skin_color=(255, 200, 140),
            hair_color=(50, 30, 20),
            shirt_color=(30, 100, 200),
            eye_color=(50, 100, 200),
            mouth_color=(200, 100, 100)
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = CartoonCharacterGenerator(Path(tmpdir))
            success = gen.generate_character('test_hero', style)
            
            assert success
            char_dir = Path(tmpdir) / 'test_hero'
            assert char_dir.exists()
            assert (char_dir / 'test_hero_neutral.png').exists()
            assert (char_dir / 'test_hero_happy.png').exists()
            assert (char_dir / 'mouths' / 'A.png').exists()
