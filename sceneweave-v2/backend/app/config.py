"""
config.py - Environment configuration and constants for SceneWeave MVP
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "SceneWeave MVP"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Paths
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", "/tmp/sceneweave/uploads"))
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "/tmp/sceneweave/output"))
    TEMP_DIR: Path = Path(os.getenv("TEMP_DIR", "/tmp/sceneweave/temp"))
    LOGS_DIR: Path = Path(os.getenv("LOGS_DIR", "./logs"))
    ASSETS_DIR: Path = Path(os.getenv("ASSETS_DIR", "./backend/assets"))
    
    # File Upload Constraints
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: list = [".txt"]
    
    # LLM Configuration (Ollama)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")
    
    # TTS Configuration (Kokoro)
    TTS_ENGINE: str = os.getenv("TTS_ENGINE", "kokoro")  # or "api" for Groq/TogetherAI
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Job Management
    MAX_CONCURRENT_JOBS: int = int(os.getenv("MAX_CONCURRENT_JOBS", "2"))
    JOB_TIMEOUT_SECONDS: int = int(os.getenv("JOB_TIMEOUT_SECONDS", "3600"))  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables

# Create global settings instance
settings = Settings()

# Create required directories
for dir_path in [settings.UPLOAD_DIR, settings.OUTPUT_DIR, settings.TEMP_DIR, settings.LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
