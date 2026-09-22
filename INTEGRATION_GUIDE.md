"""
Integration Guide: Adding $2-5 Tier to SceneWeave API

This shows how to integrate LeanVideoProcessor into your existing endpoints.py
"""

# ============================================================================
# STEP 1: Add to your imports in endpoints.py
# ============================================================================

from app.utils.lean_processor import LeanVideoProcessor

# ============================================================================
# STEP 2: Create global instance (after existing instances)
# ============================================================================

# Add after the existing instances (around line 26)
lean_processor = LeanVideoProcessor(
    job_manager=job_manager,
    tts_engine=tts_engine,
    video_composer=video_composer,
    llm_generator=None  # Optional - will use heuristics if None
)

# ============================================================================
# STEP 3: Add new endpoint for $2-5 tier
# ============================================================================

@router.post("/upload-lean", response_model=UploadResponse)
async def upload_lean(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    Upload story for $2-5 tier processing
    - Max 500 characters
    - 60-90 second video output
    - Cost optimized (~$0.15-0.30 per video)
    """
    try:
        logger.info(f"📥 Lean tier upload: {file.filename}")
        
        # Validate file
        if not file.filename.endswith('.txt'):
            raise InvalidFileTypeError(f"Only .txt files allowed, got {file.filename}")
        
        # Read file
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Validate size
        if len(text_content) > 500:
            logger.warning(f"⚠️ Story {len(text_content)} chars, truncating to 500")
            text_content = text_content[:500]
        
        if len(text_content) < 50:
            raise HTTPException(status_code=400, detail="Story too short (min 50 chars)")
        
        # Create job
        job_id = job_manager.create_job(filename=file.filename)
        logger.info(f"✅ Job created: {job_id}")
        
        # Save file
        file_path = settings.UPLOAD_DIR / f"{job_id}.txt"
        file_path.write_text(text_content)
        
        # Process in background
        if background_tasks:
            background_tasks.add_task(lean_processor.process_story, job_id, str(file_path))
        
        return UploadResponse(
            job_id=job_id,
            filename=file.filename,
            tier="$2-5",
            message=f"Processing {len(text_content)}-char story (60-90s video)"
        )
    
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# STEP 4: Test endpoint
# ============================================================================

@router.get("/test-lean")
async def test_lean(background_tasks: BackgroundTasks):
    """Test the lean processor with sample story"""
    sample_story = """
    A young girl discovers an ancient map in her grandmother's attic.
    The map leads to a hidden forest filled with magical creatures.
    She embarks on an adventure to find the legendary Crystal of Light.
    Along the way, she befriends a wise fox and learns that courage comes from within.
    Together, they unlock the forest's secrets.
    """
    
    job_id = job_manager.create_job(filename="test_lean.txt")
    file_path = settings.UPLOAD_DIR / f"{job_id}.txt"
    file_path.write_text(sample_story)
    
    if background_tasks:
        background_tasks.add_task(lean_processor.process_story, job_id, str(file_path))
    
    return {
        "job_id": job_id,
        "message": "Test job started",
        "story_length": len(sample_story),
        "tier": "$2-5",
        "expected_duration": "60-90 seconds"
    }

# ============================================================================
# OPTIONAL: Enhance get_script_generator to work with lean processor
# ============================================================================

def initialize_lean_processor_with_llm():
    """
    Initialize lean processor with LLM for enhanced analysis
    (Optional - improves tone/setting detection but adds $0.01 cost)
    """
    global lean_processor
    try:
        gen = get_script_generator()
        if gen:
            lean_processor.llm = gen
            logger.info("✅ Lean processor LLM initialized")
    except Exception as e:
        logger.warning(f"LLM initialization for lean processor failed: {e}")
        # Continues with heuristic-only mode

# Call this on startup
# initialize_lean_processor_with_llm()

# ============================================================================
# SUMMARY OF CHANGES
# ============================================================================

"""
What this adds to your API:

1. New endpoint: POST /api/upload-lean
   - Accept 500-char max stories
   - Automatic processing in background
   - Returns job_id for tracking

2. Test endpoint: GET /api/test-lean
   - Quick test with sample story
   - Useful for debugging

3. Integration with existing job tracking
   - Uses your existing JobManager
   - Uses your existing TTS engine
   - Uses your existing video composer

Cost breakdown for $2-5 tier:
  - LLM (optional): $0.01
  - TTS narration: $0.05-0.10
  - Video composition: $0.00 (local)
  - Backgrounds: $0.00 (pre-made)
  - Total: ~$0.15-0.30 per video
  
At $2-5 price: 10-30x margin ✅

Next steps:
1. Add these imports and instances to your endpoints.py
2. Add the /api/upload-lean endpoint
3. Test with /api/test-lean
4. Monitor job status with existing /api/status/{job_id}
"""
