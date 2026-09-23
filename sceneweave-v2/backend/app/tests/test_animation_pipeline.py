"""
test_animation_pipeline.py - Test the complete animation pipeline
Demonstrates how all three modules work together
"""
import logging
from pathlib import Path
from app.utils.story_analyzer import StoryAnalyzer
from app.utils.character_asset_generator import CharacterAssetGenerator
from app.utils.background_asset_generator import BackgroundAssetGenerator
from app.utils.animation_engine import AnimationEngine

logger = logging.getLogger(__name__)

def test_full_pipeline():
    """Test complete pipeline: Story → Characters → Backgrounds → Animations"""
    
    # Sample story
    story_text = """
    The Brave Knight
    
    Once there was a brave knight named Arthur who lived in a dark forest.
    Arthur said, "I must find the dragon's lair!"
    A wise wizard appeared before him.
    The wizard whispered, "I will help you, young knight."
    Arthur felt happy to have found a friend.
    Together they walked into the mysterious caves.
    """
    
    job_id = "test_001"
    output_dir = Path("/tmp/sceneweave_test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*80)
    print("🎬 SCENEWEAVE FULL PIPELINE TEST")
    print("="*80 + "\n")
    
    # Step 1: Story Analysis
    print("📖 STEP 1: Story Analysis")
    print("-" * 80)
    analyzer = StoryAnalyzer()
    screenplay = analyzer.analyze_story(story_text, job_id)
    
    print(f"✅ Title: {screenplay['title']}")
    print(f"✅ Genre: {screenplay['genre']}")
    print(f"✅ Characters found: {len(screenplay['characters'])}")
    for char in screenplay['characters']:
        print(f"   - {char['name']} ({char.get('gender', 'unknown')})")
    print(f"✅ Scenes found: {len(screenplay['scenes'])}")
    print(f"✅ Total duration: {screenplay['total_duration_seconds']:.0f} seconds")
    
    # Step 2: Character Asset Generation
    print("\n🎨 STEP 2: Character Asset Generation")
    print("-" * 80)
    char_gen = CharacterAssetGenerator(output_dir)
    
    for char in screenplay['characters']:
        char_assets = char_gen.generate_character_assets(char, job_id)
        print(f"✅ Generated assets for {char['name']}")
        print(f"   Sprites: {list(char_assets.keys())[:3]}... ({len(char_assets)} total)")
    
    # Step 3: Background Asset Generation
    print("\n🌄 STEP 3: Background Asset Generation")
    print("-" * 80)
    bg_gen = BackgroundAssetGenerator(output_dir)
    
    for idx, scene in enumerate(screenplay['scenes']):
        bg_metadata = bg_gen.generate_background(scene, job_id, idx)
        print(f"✅ Scene {idx}: {bg_metadata['setting']}")
        print(f"   Environment: {bg_metadata['environment']}, Mood: {bg_metadata['mood']}")
    
    # Step 4: Animation Engine
    print("\n🎬 STEP 4: Animation Engine")
    print("-" * 80)
    anim_engine = AnimationEngine(output_dir)
    
    for idx, scene in enumerate(screenplay['scenes']):
        animations = anim_engine.generate_scene_animations(scene, job_id, idx)
        anim_engine.save_animations(animations, job_id, idx)
        
        print(f"✅ Scene {idx} animations generated")
        print(f"   Characters animated: {list(animations['characters'].keys())}")
        for char_name, char_anim in animations['characters'].items():
            lipsync_count = len(char_anim.get('lipsync_keyframes', []))
            print(f"   - {char_name}: {lipsync_count} lip-sync keyframes")
    
    print("\n" + "="*80)
    print("✅ PIPELINE COMPLETE!")
    print("="*80)
    print(f"\nGenerated assets saved to: {output_dir}")
    print("\nNext step: Enhanced Video Composer will render these assets into final MP4")
    print("\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_full_pipeline()
