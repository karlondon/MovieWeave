"""
schemas.py - Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    """Job status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    timestamp: datetime

class UploadResponse(BaseModel):
    """File upload response"""
    job_id: str
    filename: str
    status: str = JobStatus.PENDING
    message: str
    timestamp: datetime

class JobStatusResponse(BaseModel):
    """Job status response"""
    job_id: str
    filename: str
    status: str
    progress: int = Field(0, ge=0, le=100)
    message: Optional[str] = None
    error: Optional[str] = None
    output_file: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class SceneData(BaseModel):
    """Individual scene data from LLM"""
    scene_number: int
    background_description: str
    character_id: str
    dialogue: str
    emotion: str = "neutral"

class ScriptGenerationResponse(BaseModel):
    """Script generation response"""
    job_id: str
    scenes: List[SceneData]
    total_scenes: int
    status: str = JobStatus.COMPLETED
    timestamp: datetime

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    message: str
    timestamp: datetime
    request_id: Optional[str] = None
