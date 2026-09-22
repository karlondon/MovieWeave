"""Integration test for Feature 1: Cartoon Character System"""
from pathlib import Path
from backend.cartoon_character_generator import CartoonCharacterGenerator, CharacterStyle
from backend.cartoon_character import CartoonCharacter
from backend.character_manager import CharacterManager
from backend.lip_sync_engine import LipSyncEngine

def test_feature_1_integration():
    """Complete integration test for Feature 1"""
    print("\n" + "="*60)
    print("FEATURE 1 INTEGRATION TEST: Cartoon Character System")
    print("="*60)
    
    # Test 1: Character Generation
    print("\n[1/5] Testing Character Generation...")
    assets_dir = Path("backend/assets/characters")
    
    if not assets_dir.exists():
        print("  ✗ Character assets not found. Running generator...")
        from generate_characters import main as generate_chars
        generate_chars()
    else:
        print("  ✓ Character assets directory exists")
    
    # Test 2: Character Loading
    print("\n[2/5] Testing Character Loading...")
    manager = CharacterManager(assets_dir)
    available = manager.get_available_characters()
    
    print(f"  ✓ Found {len(available)} characters")
    if len(available) == 0:
        print("  ✗ No characters found!")
        return False
    
    for char_name in available[:3]:  # Test first 3
        char = manager.load_character(char_name)
        if char:
            print(f"    ✓ Loaded: {char_name}")
        else:
            print(f"    ✗ Failed to load: {char_name}")
            return False
    
    # Test 3: Character Rendering
    print("\n[3/5] Testing Character Rendering...")
    hero = manager.load_character('hero_001')
    if hero:
        expressions = hero.get_available_expressions()
        mouths = hero.get_available_mouths()
        print(f"  ✓ hero_001 has {len(expressions)} expressions")
        print(f"  ✓ hero_001 has {len(mouths)} mouth shapes")
        
        if expressions:
            frame = hero.render_frame(expressions[0], 'A')
            if frame:
                print(f"  ✓ Successfully rendered frame")
            else:
                print(f"  ✗ Failed to render frame")
                return False
    else:
        print("  ✗ Could not load hero_001")
        return False
    
    # Test 4: Lip Sync Engine
    print("\n[4/5] Testing Lip Sync Engine...")
    engine = LipSyncEngine()
    events = engine.extract_mouth_shapes()
    print(f"  ✓ Generated {len(events)} lip-sync events")
    
    valid_mouths = ['A', 'E', 'I', 'O', 'U', 'MBP', 'X']
    all_valid = all(e.mouth_shape in valid_mouths for e in events)
    if all_valid:
        print(f"  ✓ All mouth shapes are valid")
    else:
        print(f"  ✗ Invalid mouth shapes detected")
        return False
    
    # Test 5: Character Variety
    print("\n[5/5] Testing Character Variety...")
    char_types = {}
    for char_name in available:
        char_type = char_name.split('_')[0]
        char_types[char_type] = char_types.get(char_type, 0) + 1
    
    print(f"  ✓ Generated character types:")
    for char_type, count in sorted(char_types.items()):
        print(f"    - {char_type}: {count} characters")
    
    # Summary
    print("\n" + "="*60)
    print("✅ FEATURE 1 INTEGRATION TEST PASSED")
    print("="*60)
    print(f"✓ Total characters: {len(available)}")
    print(f"✓ Character types: {len(char_types)}")
    print(f"✓ Lip-sync events: {len(events)}")
    print("\nReady for Feature 2: Cartoon Video Engine Integration")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_feature_1_integration()
    exit(0 if success else 1)
