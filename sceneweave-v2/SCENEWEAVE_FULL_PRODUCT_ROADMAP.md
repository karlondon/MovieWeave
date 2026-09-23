# 🎬 SceneWeave Full Product Roadmap
## From MVP to Toonbee.ai Competitor

**Status**: Planning Phase 2A - Core Story-to-Visual Pipeline  
**Target Duration**: 6 weeks for complete production-ready product  

---

## 📊 Current State vs. Target

### ❌ Current Limitations
- Only 31-second videos with voice-only output
- No character sprites or animations
- No scene-specific visuals beyond static backgrounds
- Single character/narrator only

### ✅ Target Capabilities
- Full story analysis with character extraction & animation descriptors
- Character sprite generation & animated sprite system
- Multi-scene video composition with transitions
- Production-grade React frontend
- 2-5+ minute videos with multiple characters

---

## 🏗️ Architecture Overview

```
Story Input
    ↓
[Story Analyzer] - Extract characters, scenes, emotions, durations
    ↓
[Asset Generator] - Create/fetch character sprites & backgrounds
    ↓
[Animation Engine] - Generate keyframes, lip-sync, gestures
    ↓
[Video Composer] - Multi-character, multi-scene video generation
    ↓
[React Frontend] - Upload, customize, preview, download
```

---

## 📋 Phase 2A: Story-to-Visual Pipeline

### Key Components

1. **story_analyzer.py** - Extract character profiles, scenes, dialogue with emotion
2. **character_asset_generator.py** - Convert descriptions → sprite assets
3. **background_asset_generator.py** - Scene descriptions → background images
4. **animation_engine.py** - Text → lip-sync visemes → keyframes → character movements
5. **enhanced_video_composer.py** - Multi-character animation + scene transitions

### Story Analyzer Output
```json
{
  "title": "The Brave Knight",
  "genre": "fantasy",
  "characters": [{
    "name": "Arthur",
    "age": "25",
    "gender": "male",
    "voice_type": "baritone",
    "personality_traits": ["brave", "noble"],
    "color_palette": ["#4169E1", "#87CEEB"]
  }],
  "scenes": [{
    "setting": "Dark forest",
    "lighting": "dim",
    "mood": "mysterious",
    "duration_seconds": 45.5,
    "dialogue_lines": [{
      "character": "Arthur",
      "text": "I must find the dragon's lair.",
      "emotion": "determined"
    }]
  }],
  "total_duration_seconds": 180
}
```

---

## 🚀 Implementation Timeline

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1 | Story Analysis | Character/scene extraction, dialogue timing |
| 1-2 | Asset Generation | Character sprites, backgrounds library |
| 2 | Animation | Lip-sync engine, keyframe generation |
| 3 | Video Composition | Multi-character rendering, transitions |
| 4-5 | Frontend UI | Upload, preview, customization |
| 5-6 | Polish & Deploy | Testing, optimization, deployment |

---

## 📁 File Structure

```
/backend/app/utils/
├── story_analyzer.py              [NEW]
├── character_asset_generator.py   [NEW]
├── background_asset_generator.py  [NEW]
├── animation_engine.py            [NEW]
├── enhanced_video_composer.py     [NEW]
├── viseme_mapper.py               [NEW] - Text to phonemes
└── asset_manager.py               [NEW] - Asset caching
```

---

## 🎯 Success Criteria

- ✅ Extract characters, scenes, emotions from any story
- ✅ Generate character sprites with expressions
- ✅ Create 2-5 minute videos with proper lip-sync
- ✅ Support multiple characters in same scene
- ✅ Professional-grade frontend UI
- ✅ Performance: <2 min per video generation

**This is the roadmap for a production-ready competitor to Toonbee.ai!**
