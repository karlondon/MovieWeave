"""
file_handler.py - File upload and text extraction utilities
"""
import os
from pathlib import Path
from typing import Tuple
import uuid
from datetime import datetime
import logging

from app.config import settings
from app.utils.errors import (
    FileSizeError, InvalidFileTypeError, TextExtractionError, FileUploadError
)

logger = logging.getLogger(__name__)

class FileHandler:
    """Handle file uploads and text extraction"""
    
    @staticmethod
    def validate_file(filename: str, file_size: int) -> None:
        """
        Validate uploaded file
        
        Args:
            filename: Name of the file
            file_size: Size of the file in bytes
            
        Raises:
            FileSizeError: If file exceeds size limit
            InvalidFileTypeError: If file type is not supported
        """
        # Check file size
        if file_size > settings.MAX_FILE_SIZE:
            raise FileSizeError(
                f"File size {file_size} bytes exceeds maximum {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Check file extension
        file_ext = Path(filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            allowed = ", ".join(settings.ALLOWED_EXTENSIONS)
            raise InvalidFileTypeError(
                f"File type '{file_ext}' not supported. Allowed: {allowed}"
            )
        
        logger.info(f"✅ File validation passed: {filename} ({file_size} bytes)")
    
    @staticmethod
    def save_uploaded_file(content: bytes, original_filename: str) -> Tuple[str, Path]:
        """
        Save uploaded file to disk
        
        Args:
            content: File content as bytes
            original_filename: Original filename from upload
            
        Returns:
            Tuple of (job_id, file_path)
            
        Raises:
            FileUploadError: If save operation fails
        """
        try:
            # Generate unique job ID
            job_id = str(uuid.uuid4())
            
            # Create unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{job_id}_{timestamp}{Path(original_filename).suffix}"
            
            # Save to upload directory
            file_path = settings.UPLOAD_DIR / safe_filename
            
            with open(file_path, 'wb') as f:
                f.write(content)
            
            logger.info(f"✅ File saved: {file_path} (Job ID: {job_id})")
            return job_id, file_path
            
        except Exception as e:
            logger.error(f"❌ Failed to save file: {str(e)}")
            raise FileUploadError(f"Failed to save uploaded file: {str(e)}")
    
    @staticmethod
    def extract_text_from_file(file_path: Path) -> str:
        """
        Extract text from uploaded file
        
        Args:
            file_path: Path to the uploaded file
            
        Returns:
            Extracted text content
            
        Raises:
            TextExtractionError: If extraction fails
        """
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            file_ext = file_path.suffix.lower()
            
            if file_ext == ".txt":
                text = FileHandler._extract_from_txt(file_path)
            else:
                raise InvalidFileTypeError(f"Unsupported file type: {file_ext}")
            
            if not text.strip():
                raise TextExtractionError("Extracted text is empty")
            
            logger.info(f"✅ Text extracted from {file_path.name}: {len(text)} characters")
            return text
            
        except TextExtractionError:
            raise
        except Exception as e:
            logger.error(f"❌ Text extraction failed: {str(e)}")
            raise TextExtractionError(f"Failed to extract text: {str(e)}")
    
    @staticmethod
    def _extract_from_txt(file_path: Path) -> str:
        """Extract text from .txt file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text
        except UnicodeDecodeError:
            # Try alternative encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                text = f.read()
            return text
    
    @staticmethod
    def cleanup_file(file_path: Path) -> None:
        """
        Delete uploaded file (cleanup)
        
        Args:
            file_path: Path to file to delete
        """
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"🗑️  Cleaned up: {file_path}")
        except Exception as e:
            logger.warning(f"⚠️  Failed to cleanup {file_path}: {str(e)}")
