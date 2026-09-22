"""
main.py - FastAPI application entry point for SceneWeave MVP
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
import logging

from app.config import settings
from app.utils.logger import setup_logging
from app.utils.errors import SceneWeaveError
from app.api import endpoints
from app.api import hybrid_endpoints

# Setup logging
logger = setup_logging(settings.LOGS_DIR, app_name="sceneweave")

# ============================================================================
# LIFESPAN EVENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    # Startup
    logger.info("=" * 80)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📁 Upload Dir: {settings.UPLOAD_DIR}")
    logger.info(f"📁 Output Dir: {settings.OUTPUT_DIR}")
    logger.info(f"📁 Temp Dir: {settings.TEMP_DIR}")
    logger.info(f"🤖 LLM: {settings.OLLAMA_MODEL} @ {settings.OLLAMA_BASE_URL}")
    logger.info("=" * 80)
    
    yield
    
    # Shutdown
    logger.info("=" * 80)
    logger.info(f"🛑 Shutting down {settings.APP_NAME}")
    logger.info("=" * 80)

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=settings.APP_NAME,
    description="Lean MVP for text-to-video generation using Ollama + Kokoro TTS",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# ============================================================================
# MIDDLEWARE
# ============================================================================

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(SceneWeaveError)
async def sceneweave_exception_handler(request: Request, exc: SceneWeaveError):
    """Handle SceneWeaveError exceptions"""
    logger.error(f"❌ {exc.__class__.__name__}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"❌ Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ============================================================================
# ROUTES
# ============================================================================

# Include API routes
app.include_router(endpoints.router)
app.include_router(hybrid_endpoints.router)

@app.get("/")
async def root():
    """Root endpoint - API documentation"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "frontend": "/ui",
        "endpoints": {
            "health": "GET /api/health",
            "upload": "POST /api/upload",
            "status": "GET /api/status/{job_id}",
            "jobs": "GET /api/jobs"
        }
    }

# ============================================================================
# STATIC FILES & FRONTEND
# ============================================================================

# Mount static files (CSS, JS, etc.) - MUST come BEFORE catch-all routes
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    logger.info(f"✅ Serving static files from: {static_dir}")
else:
    logger.warning(f"⚠️ Static directory not found: {static_dir}")

# Serve index.html for SPA routing
@app.get("/ui", include_in_schema=False)
async def serve_ui_root():
    """Serve the React frontend UI"""
    index_path = Path(__file__).parent.parent / "static" / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    return JSONResponse({"error": "Frontend not found"}, status_code=404)

# Catch-all route for SPA - MUST come LAST
@app.get("/{path:path}", include_in_schema=False)
async def serve_frontend(path: str):
    """Serve frontend assets or index.html for SPA routing"""
    # Don't serve API or docs routes through this handler
    if path.startswith(("api/", "docs", "redoc", "openapi.json")):
        return JSONResponse({"error": "Not found"}, status_code=404)
    
    file_path = Path(__file__).parent.parent / "static" / path
    
    # If file exists and is a file, serve it
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    
    # Otherwise serve index.html for React routing
    index_path = Path(__file__).parent.parent / "static" / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    
    return JSONResponse({"error": "Not found"}, status_code=404)

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

