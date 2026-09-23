# ⚠️ SceneWeave v2 - ABANDONED PROOF OF CONCEPT

**Status:** `DISCONTINUED` | **Date:** September 23, 2026 | **Reason:** Architectural Failure

---

## What This Project Was

SceneWeave v2 was an attempt to build a **text-to-animated-video** platform similar to Toonbee.

### Claimed Features
- 6-stage video generation pipeline
- AI-powered story analysis (via Groq LLM)
- Character asset generation with animation
- Background scene generation
- Animation engine with sprite rendering
- Text-to-speech audio synthesis (Kokoro TTS)
- FFmpeg-based video composition

---

## Why It Was Abandoned

### Critical Architectural Flaw

After a complete code audit, this project was found to be **fundamentally non-functional** for its stated purpose.

#### Problem 1: No Actual Animation
The "animation engine" does not animate. It takes ONE static image and copies it 720 times (for 30 seconds at 24fps).

#### Problem 2: Character Generation is Geometric Shapes
Characters are colored circles and rectangles—not actual sprites or rigged models.

#### Problem 3: Fake Progress Reporting
Progress bar updates without performing the claimed work.

#### Problem 4: Output Quality
Generated videos are slideshows:
- 1 static background image for entire scene
- Zero character animation or movement
- Single TTS voiceover
- No visual effects or transitions

---

## What Would Be Required to Fix This

### Missing Components
1. **2D Character Rigging** - Skeletal animation, IK, facial morphing
2. **Sprite Frame Generation** - 6-12+ distinct poses per emotion
3. **Mouth Movement Sync** - Frame-by-frame lip-sync to phonemes
4. **Scene Camera Logic** - Pan, zoom, parallax layering
5. **Real Asset Generation** - ML-based image synthesis
6. **Dynamic Transitions** - Professional video effects

### Realistic Options
- **Third-party APIs:** $0.10-$1.00 per video (Runway ML, Replicate)
- **Local rendering:** 5-10 minutes per video, requires expertise
- **Hybrid approach:** Manual sprite assembly + AI video generation

---

## Lessons Learned

1. Demand real output, not fake progress
2. Animation is hard—don't underestimate complexity
3. Know your hardware limits
4. Third-party APIs often beat custom implementations
5. Validate architecture before writing thousands of lines

---

## Code Status

- ❌ Non-functional for its stated purpose
- ⚠️ Not maintained
- 🔴 Not recommended for use
- 📚 Reference only for what NOT to do

---

**Abandoned:** September 23, 2026  
**Reason:** Produces static images + audio, not animated video  
**Recommendation:** Use third-party APIs (Runway ML, Replicate, Stable Video Diffusion)
