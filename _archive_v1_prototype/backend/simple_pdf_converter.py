"""simple_pdf_converter.py - Simple PDF to video converter"""
from pathlib import Path
import logging
from typing import List, Tuple
import subprocess

logger = logging.getLogger(__name__)

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("PyPDF2 not installed")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logger.warning("pyttsx3 not installed")


class SimplePDFConverter:
    """Convert PDF/TXT to video with rotating characters"""
    
    def __init__(self, output_folder: Path):
        self.output_folder = output_folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
    
    def extract_text(self, file_path: Path) -> str:
        """Extract text from PDF or TXT"""
        if file_path.suffix.lower() == '.pdf':
            return self._extract_pdf(file_path)
        elif file_path.suffix.lower() in ['.txt', '.text']:
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_path.suffix}")
    
    def _extract_pdf(self, file_path: Path) -> str:
        """Extract text from PDF"""
        if not PDF_AVAILABLE:
            raise RuntimeError("PyPDF2 not installed")
        
        try:
            text = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise RuntimeError(f"PDF extraction failed: {e}")
    
    def _extract_txt(self, file_path: Path) -> str:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def split_text_into_lines(self, text: str, max_lines: int = 30) -> List[str]:
        """Split text into dialogue lines"""
        # Clean text
        text = ' '.join(text.split())
        
        # Split by sentences
        lines = []
        current = ""
        for char in text:
            current += char
            if char in '.!?':
                line = current.strip()
                if len(line) > 10:  # Skip very short lines
                    lines.append(line)
                current = ""
        
        if current.strip():
            lines.append(current.strip())
        
        # Limit lines
        if len(lines) > max_lines:
            lines = lines[:max_lines]
        
        return lines
    
    def generate_audio(self, text: str, output_file: Path, voice_id: int = 0) -> bool:
        """Generate audio from text using pyttsx3"""
        if not TTS_AVAILABLE:
            logger.warning("pyttsx3 not available, skipping audio generation")
            return False
        
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            voices = engine.getProperty('voices')
            if voice_id < len(voices):
                engine.setProperty('voice', voices[voice_id].id)
            
            engine.save_to_file(text, str(output_file))
            engine.runAndWait()
            
            return output_file.exists()
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            return False
    
    def get_audio_duration(self, audio_file: Path) -> float:
        """Get audio duration in seconds"""
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1',
                 str(audio_file)],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return float(result.stdout.strip())
        except Exception as e:
            logger.warning(f"Could not get audio duration: {e}")
        return 2.0
