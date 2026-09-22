"""render_videos.py - Render sample cartoon videos with Feature 2"""

from pathlib import Path
from backend.cartoon_video_engine import CartoonVideoEngine
from backend.character_manager import CharacterManager

def render_sample_videos():
    """Render sample videos for demonstration"""
    print("\n" + "="*70)
    print("FEATURE 2: CARTOON VIDEO ENGINE - SAMPLE RENDERING")
    print("="*70 + "\n")
    
    # Initialize engine
    engine = CartoonVideoEngine(
        character_dir=Path("backend/assets/characters"),
        output_dir=Path("output/videos")
    )
    
    # Get available characters
    manager = CharacterManager(Path("backend/assets/characters"))
    chars = manager.get_available_characters()
    
    if not chars:
        print("❌ No characters found. Run generate_characters.py first!")
        return False
    
    print(f"✓ Found {len(chars)} characters\n")
    
    # Sample 1: Render first character with different expressions
    print("Sample 1: Rendering expressions...\n")
    char_name = chars[0]
    
    for expr in ['neutral', 'happy', 'sad', 'angry']:
        output_file = Path(f"output/videos/{char_name}_{expr}.mp4")
        success = engine.render_dialogue_video(
            character_name=char_name,
            expression=expr,
            duration_seconds=2.0,
            output_file=output_file
        )
        status = "✓" if success else "✗"
        print(f"  {status} {char_name}_{expr}.mp4")
    
    # Sample 2: Create animation gallery
    print("\nSample 2: Creating animation gallery...\n")
    gallery_success = engine.create_animation_gallery()
    
    if gallery_success:
        print("  ✓ Gallery created at: output/videos/gallery/")
    
    # Summary
    print("\n" + "="*70)
    print("VIDEO RENDERING COMPLETE!")
    print("="*70)
    print("\nOutput files:")
    print(f"  📁 output/videos/{char_name}_neutral.mp4")
    print(f"  📁 output/videos/{char_name}_happy.mp4")
    print(f"  📁 output/videos/{char_name}_sad.mp4")
    print(f"  📁 output/videos/{char_name}_angry.mp4")
    print(f"  📁 output/videos/gallery/")
    
    print("\nTo play videos:")
    print(f"  open output/videos/{char_name}_happy.mp4")
    print("\nOr use FFmpeg:")
    print(f"  ffplay output/videos/{char_name}_happy.mp4")
    print("\n" + "="*70 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        render_sample_videos()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. FFmpeg is installed: brew install ffmpeg")
        print("  2. Characters exist: python generate_characters.py")
