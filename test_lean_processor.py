#!/usr/bin/env python3
"""
test_lean_processor.py - Standalone test for $2-5 tier video generation
Run this to test the lean processor locally before deploying to server
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "sceneweave-v2" / "backend"
sys.path.insert(0, str(backend_path))

from app.config import settings
from app.utils.job_manager import JobManager
from app.utils.tts_engine import KokoroTTSEngine
from app.utils.video_composer import FFmpegVideoComposer
from app.utils.lean_processor import LeanVideoProcessor

# Sample story (500 chars max)
SAMPLE_STORY = """
A young girl discovers an ancient map in her grandmother's attic.
The map leads to a hidden forest filled with magical creatures.
She embarks on an adventure to find the legendary Crystal of Light.
Along the way, she befriends a wise fox and learns that courage
comes from within. Together, they unlock the forest's secrets.
"""

def test_lean_processor():
    """Test the lean processor with sample story"""
    print("=" * 70)
    print("🧪 TESTING LEAN VIDEO PROCESSOR ($2-5 TIER)")
    print("=" * 70)
    
    # Validate story length
    print(f"\n📖 Story length: {len(SAMPLE_STORY)} chars")
    if len(SAMPLE_STORY) > 500:
        print("❌ Story too long! Max 500 chars")
        return False
    
    # Initialize components
    print("\n🔧 Initializing components...")
    try:
        job_manager = JobManager()
        tts_engine = KokoroTTSEngine(settings.OUTPUT_DIR)
        video_composer = FFmpegVideoComposer(settings.OUTPUT_DIR, settings.TEMP_DIR)
        processor = LeanVideoProcessor(
            job_manager=job_manager,
            tts_engine=tts_engine,
            video_composer=video_composer,
            llm_generator=None
        )
        print("✅ All components initialized")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False
    
    # Create test job
    print("\n📝 Creating test job...")
    job_id = "test_lean_001"
    test_file = settings.UPLOAD_DIR / f"{job_id}.txt"
    test_file.write_text(SAMPLE_STORY)
    print(f"✅ Test file created: {test_file}")
    
    # Process story
    print("\n🎬 Processing story...")
    print("-" * 70)
    success = processor.process_story(job_id, str(test_file))
    print("-" * 70)
    
    if success:
        # Check output
        job = job_manager.get_job(job_id)
        print(f"\n✅ PROCESSING COMPLETE!")
        print(f"Job ID: {job_id}")
        print(f"Status: {job['status']}")
        print(f"Progress: {job['progress']}%")
        print(f"Message: {job['message']}")
        if job.get('output_file'):
            print(f"Output: {job['output_file']}")
            output_size_mb = Path(job['output_file']).stat().st_size / (1024*1024)
            print(f"File size: {output_size_mb:.1f} MB")
        return True
    else:
        print(f"\n❌ PROCESSING FAILED")
        job = job_manager.get_job(job_id)
        print(f"Error: {job.get('error')}")
        return False

if __name__ == "__main__":
    success = test_lean_processor()
    sys.exit(0 if success else 1)
