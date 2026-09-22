"""Extended character types - Superheroes, Pirates, Aliens, Robots, etc."""
from pathlib import Path
from backend.cartoon_character_generator import CartoonCharacterGenerator, CharacterStyle
import random

class CharacterTypeGenerator:
    """Generate diverse character types"""
    
    @staticmethod
    def get_superhero_style() -> CharacterStyle:
        return CharacterStyle(
            skin_color=(255, 200, 140),
            hair_color=(50, 30, 20),
            shirt_color=random.choice([(30, 100, 200), (200, 30, 30), (30, 150, 30)]),
            eye_color=(50, 100, 200),
            mouth_color=(200, 100, 100)
        )
    
    @staticmethod
    def get_pirate_style() -> CharacterStyle:
        return CharacterStyle(
            skin_color=(240, 180, 100),
            hair_color=(60, 40, 20),
            shirt_color=(80, 60, 40),
            eye_color=(100, 50, 20),
            mouth_color=(180, 80, 80)
        )
    
    @staticmethod
    def get_alien_style() -> CharacterStyle:
        return CharacterStyle(
            skin_color=(100, 200, 100),
            hair_color=(150, 200, 150),
            shirt_color=(50, 100, 150),
            eye_color=(200, 100, 200),
            mouth_color=(150, 150, 50)
        )
    
    @staticmethod
    def get_robot_style() -> CharacterStyle:
        return CharacterStyle(
            skin_color=(180, 180, 180),
            hair_color=(100, 100, 100),
            shirt_color=(150, 150, 150),
            eye_color=(255, 200, 0),
            mouth_color=(200, 100, 0)
        )
    
    @staticmethod
    def get_wizard_style() -> CharacterStyle:
        return CharacterStyle(
            skin_color=(255, 200, 140),
            hair_color=(100, 50, 150),
            shirt_color=(100, 50, 150),
            eye_color=(100, 200, 200),
            mouth_color=(200, 100, 100)
        )
    
    @staticmethod
    def get_princess_style() -> CharacterStyle:
        return CharacterStyle(
            skin_color=(255, 220, 170),
            hair_color=(255, 200, 100),
            shirt_color=(255, 100, 150),
            eye_color=(150, 100, 200),
            mouth_color=(255, 100, 120)
        )
    
    @staticmethod
    def get_knight_style() -> CharacterStyle:
        return CharacterStyle(
            skin_color=(240, 180, 120),
            hair_color=(80, 50, 30),
            shirt_color=(150, 150, 150),
            eye_color=(80, 80, 80),
            mouth_color=(180, 80, 80)
        )
    
    @staticmethod
    def get_monster_style() -> CharacterStyle:
        return CharacterStyle(
            skin_color=(100, 150, 100),
            hair_color=(50, 100, 50),
            shirt_color=(80, 120, 80),
            eye_color=(255, 100, 0),
            mouth_color=(200, 50, 50)
        )


def generate_extended_types():
    """Generate one character of each type"""
    generator = CartoonCharacterGenerator(Path("backend/assets/characters"))
    
    types = {
        'superhero': CharacterTypeGenerator.get_superhero_style,
        'pirate': CharacterTypeGenerator.get_pirate_style,
        'alien': CharacterTypeGenerator.get_alien_style,
        'robot': CharacterTypeGenerator.get_robot_style,
        'wizard': CharacterTypeGenerator.get_wizard_style,
        'princess': CharacterTypeGenerator.get_princess_style,
        'knight': CharacterTypeGenerator.get_knight_style,
        'monster': CharacterTypeGenerator.get_monster_style,
    }
    
    print("\nGenerating Extended Character Types...\n")
    
    for char_type, style_func in types.items():
        style = style_func()
        success = generator.generate_character(f"{char_type}_001", style)
        print(f"  ✓ {char_type:12}" if success else f"  ✗ {char_type}")
    
    print(f"\n✓ Generated {len(types)} new character types!\n")


if __name__ == "__main__":
    generate_extended_types()
