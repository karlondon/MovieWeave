# MovieWeave Versioning & Release Strategy

## Current Versions

### ✅ Stable V1.0.0 (Production Ready)
**Released:** September 21, 2026
**Git Tag:** `v1.0.0`

**Features:**
- ✅ PDF text extraction
- ✅ AWS Polly text-to-speech
- ✅ FFmpeg-based MP4 video generation (24 FPS)
- ✅ Stick figure animation with basic movements
- ✅ Frame-by-frame subtitle rendering
- ✅ Async video generation with thread pool
- ✅ S3 upload for input PDFs
- ✅ MP3 + MP4 download support

**Performance:**
- PDF processing: < 1 minute
- Audio generation: 1-2 minutes (AWS Polly)
- Video generation: 3-5 minutes (4000+ frames)
- Total per document: 5-10 minutes

---

## Upcoming: V2.0.0 Development Roadmap

### Feature 1: Cartoon Character Assets & System
**Branch:** `feature/cartoon-characters-v2`
**Status:** Starting Now
**ETA:** Week 1-2

**Deliverable:** Fully functional cartoon character system with automatic lip-sync

### Feature 2: Cartoon Video Engine Integration
**Branch:** `feature/cartoon-engine-v2`
**Status:** Pending (After Feature 1)
**ETA:** Week 2-3

**Deliverable:** Fully integrated cartoon video generation replacing stick figures

### Feature 3: Story Format & Multi-Character Support
**Branch:** `feature/story-format-v2`
**Status:** Pending (After Feature 2)
**ETA:** Week 3-4

**Deliverable:** Support for rich story format with multiple characters and scenes

### Feature 4: Advanced Animation Features
**Branch:** `feature/advanced-animation-v2`
**Status:** Pending (After Feature 3)
**ETA:** Week 4-5

**Deliverable:** Professional-grade animation with rich expressions and effects

---

## Git Branching Strategy

```
main (production) → v1.0.0 tagged
develop (staging) 
  ├─ feature/cartoon-characters-v2 (Feature 1)
  ├─ feature/cartoon-engine-v2 (Feature 2)
  ├─ feature/story-format-v2 (Feature 3)
  └─ feature/advanced-animation-v2 (Feature 4)
```

**When complete:** Merge all to main and tag as v2.0.0

---

## Version History

| Version | Date | Status | Key Features |
|---------|------|--------|----------|
| v1.0.0 | 2026-09-21 | ✅ Stable | Stick figures, FFmpeg, Polly TTS |
| v2.0.0 | TBD | 🔄 In Dev | Cartoon chars, lip-sync, expressions |
