# 🎬 SceneWeave MVP v2.0.0

**Lean, cost-optimized text-to-video generation platform**

Convert text stories into animated videos using open-source AI tools (Ollama LLM + Kokoro TTS + FFmpeg).

---

## 📋 Project Overview

### What is SceneWeave MVP?

SceneWeave MVP is a **minimal viable product** designed to demonstrate end-to-end text-to-video generation with:

- **Lightweight Architecture**: Runs on a single CPU-only AWS instance (t3.medium or better)
- **Open-Source Stack**: 
  - Ollama for LLM (Qwen-2.5-Instruct)
  - Kokoro-82M for TTS
  - FFmpeg for video composition
  - FastAPI backend + React frontend
- **Cost-Optimized**: ~$20-30/month on AWS (vs. $500+ for GPU-heavy setups)

### Phase 1 Goals

✅ File upload and text extraction (.txt files)  
✅ LLM-based script generation (JSON structured output)  
✅ Audio generation (Kokoro TTS)  
✅ Video composition (FFmpeg sprite overlays)  
✅ Real-time job tracking and progress monitoring
