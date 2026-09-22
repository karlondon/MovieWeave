"""
errors.py - Custom exceptions and error handling for SceneWeave MVP
"""
from fastapi import HTTPException, status
from typing import Optional

class SceneWeaveError(Exception):
    """Base exception for SceneWeave application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class FileUploadError(SceneWeaveError):
    """Raised when file upload fails"""
    def __init__(self, message: str = "File upload failed"):
        super().__init__(message, status_code=400)

class FileSizeError(SceneWeaveError):
    """Raised when file size exceeds limit"""
    def __init__(self, message: str = "File size exceeds maximum allowed"):
        super().__init__(message, status_code=413)

class InvalidFileTypeError(SceneWeaveError):
    """Raised when file type is not supported"""
    def __init__(self, message: str = "File type not supported"):
        super().__init__(message, status_code=400)

class TextExtractionError(SceneWeaveError):
    """Raised when text extraction fails"""
    def __init__(self, message: str = "Failed to extract text from file"):
        super().__init__(message, status_code=422)

class LLMError(SceneWeaveError):
    """Raised when LLM service fails"""
    def __init__(self, message: str = "LLM service error"):
        super().__init__(message, status_code=503)

class JobNotFoundError(SceneWeaveError):
    """Raised when job is not found"""
    def __init__(self, job_id: str):
        super().__init__(f"Job {job_id} not found", status_code=404)

class JobProcessingError(SceneWeaveError):
    """Raised when job processing fails"""
    def __init__(self, message: str = "Job processing failed"):
        super().__init__(message, status_code=500)

def sceneweave_exception_handler(exc: SceneWeaveError):
    """Convert SceneWeaveError to HTTPException"""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "error": exc.__class__.__name__,
            "message": exc.message
        }
    )
