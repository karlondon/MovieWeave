"""FEATURE 2: Cartoon Video Engine - Usage Guide"""

from pathlib import Path
from backend.cartoon_video_engine import CartoonVideoEngine

# Initialize video engine
engine = CartoonVideoEngine(
    character_dir=Path("backend/assets/characters"),
    output_dir=Path("output/videos")
)

print(f"Video Engine: {engine}")
print(f"FPS: {engine.FPS}, Codec: {engine.VIDEO_CODEC}")

# ============================================================================
# 1. RENDER DIALOGUE VIDEO
# ============================================================================

# Render 3-second video of happy hero
success = engine.render_dialogue_video(
    character_name='hero_001',
    expression='happy',
    duration_seconds=3.0,
    output_file=Path("output/videos/hero_greeting.mp4")
)

if success:
    print("✓ Video created: hero_greeting.mp4")

# ============================================================================
# 2. RENDER WITH AUDIO
# ============================================================================

success = engine.render_dialogue_video(
    character_name='hero_001',
    expression='neutral',
    duration_seconds=5.0,
    audio_file=Path("audio/dialogue.mp3"),
    output_file=Path("output/videos/hero_with_audio.mp4")
)

# ============================================================================
# 3. RENDER ALL EXPRESSIONS
# ============================================================================

for expr in ['neutral', 'happy', 'sad', 'angry']:
    engine.render_dialogue_video(
        character_name='hero_001',
        expression=expr,
        duration_seconds=2.0,
        output_file=Path(f"output/videos/hero_{expr}.mp4")
    )

# ============================================================================
# 4. CREATE ANIMATION GALLERY
# ============================================================================

engine.create_animation_gallery()
print(f"✓ Gallery created: {engine.output_dir / 'gallery'}")

# ============================================================================
# 5. BATCH RENDER ALL CHARACTERS
# ============================================================================

def render_all_characters():
    chars = engine.manager.get_available_characters()
    print(f"\nRendering {len(chars)} character videos...\n")
    
    for char_name in chars:
        success = engine.render_dialogue_video(
            character_name=char_name,
            expression='happy',
            duration_seconds=2.0,
            output_file=engine.output_dir / f"{char_name}_demo.mp4"
        )
        print(f"  {'✓' if success else '✗'} {char_name}")

# render_all_characters()
