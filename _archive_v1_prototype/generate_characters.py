#!/usr/bin/env python3
"""Generate sample cartoon characters"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from backend.cartoon_character_generator import CartoonCharacterGenerator, CharacterStyle

def main():
    print("=" * 60)
    print("MovieWeave Cartoon Character Generator")
    print("=" * 60)
    
    assets_dir = Path(__file__).parent / "backend" / "assets" / "characters"
    generator = CartoonCharacterGenerator(assets_dir)
    
    print(f"\nGenerating characters in: {assets_dir}\n")
    
    characters = [
        ("hero_001", "hero"),
        ("hero_002", "hero"),
        ("hero_003", "hero"),
        ("hero_004", "hero"),
        ("villain_001", "villain"),
        ("villain_002", "villain"),
        ("villain_003", "villain"),
        ("child_001", "child"),
        ("child_002", "child"),
        ("child_003", "child"),
    ]
    
    generated = 0
    for char_name, char_type in characters:
        style = CartoonCharacterGenerator.get_random_style(char_type)
        success = generator.generate_character(char_name, style)
        
        if success:
            print(f"✓ {char_name:15} ({char_type:8})")
            generated += 1
        else:
            print(f"✗ {char_name:15} ({char_type:8}) - FAILED")
    
    print()
    print("=" * 60)
    print(f"Successfully generated {generated}/{len(characters)} characters")
    print("=" * 60)
    
    if assets_dir.exists():
        char_dirs = sorted([d.name for d in assets_dir.iterdir() if d.is_dir()])
        print(f"\nGenerated characters:")
        for char_dir in char_dirs:
            char_path = assets_dir / char_dir
            expressions = len([f for f in char_path.glob("*.png")])
            mouths = len(list((char_path / "mouths").glob("*.png"))) if (char_path / "mouths").exists() else 0
            print(f"  ✓ {char_dir:15} - {expressions} expressions + {mouths} mouth shapes")
    
    print()
    return 0 if generated == len(characters) else 1

if __name__ == "__main__":
    sys.exit(main())
