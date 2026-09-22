"""text_processor.py - Extract and process text from PDF and TXT files"""
import os
from pathlib import Path
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("PyPDF2 not installed. PDF support disabled.")


class TextProcessor:
    """Extract and process text from files"""
    
    def __init__(self):
        self.max_file_size = 50 * 1024 * 1024  # 50MB
    
    def extract_text(self, file_path: Path) -> str:
        """Extract text from PDF or TXT file"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = file_path.stat().st_size
        if file_size > self.max_file_size:
            raise ValueError(f"File too large. Max: {self.max_file_size/1024/1024}MB")
        
        if file_path.suffix.lower() == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.txt', '.text']:
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        if not PDF_AVAILABLE:
            raise RuntimeError("PDF support not available. Install PyPDF2.")
        
        try:
            text = ""
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                raise ValueError("No text found in PDF")
            
            return text
        except Exception as e:
            raise RuntimeError(f"Failed to extract PDF: {str(e)}")
    
    def _extract_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
            
            if not text.strip():
                raise ValueError("File is empty")
            
            return text
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as txt_file:
                text = txt_file.read()
            return text
        except Exception as e:
            raise RuntimeError(f"Failed to read text file: {str(e)}")
    
    def split_into_sentences(self, text: str, max_sentences: int = 50) -> List[str]:
        """
        Split text into sentences for character dialogue
        Limits to max_sentences to avoid extremely long videos
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Simple sentence splitting on . ! ?
        sentences = []
        current = ""
        
        for char in text:
            current += char
            if char in '.!?':
                sentence = current.strip()
                if sentence:
                    sentences.append(sentence)
                current = ""
        
        # Add remaining text
        if current.strip():
            sentences.append(current.strip())
        
        # Limit to max_sentences
        if len(sentences) > max_sentences:
            logger.warning(f"Truncating {len(sentences)} sentences to {max_sentences}")
            sentences = sentences[:max_sentences]
        
        return sentences
    
    def split_into_paragraphs(self, text: str, max_paragraphs: int = 20) -> List[str]:
        """
        Split text into paragraphs for character dialogue
        Limits to max_paragraphs to avoid extremely long videos
        """
        # Split by double newline or paragraph breaks
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if len(paragraphs) > max_paragraphs:
            logger.warning(f"Truncating {len(paragraphs)} paragraphs to {max_paragraphs}")
            paragraphs = paragraphs[:max_paragraphs]
        
        return paragraphs
    
    def create_dialogue_script(self, text: str, characters: List[str], 
                              split_by: str = 'sentences') -> List[Tuple[str, str]]:
        """
        Create a dialogue script by assigning characters to text chunks
        Returns list of (character_name, dialogue) tuples
        """
        if not characters:
            raise ValueError("No characters available")
        
        if split_by == 'sentences':
            chunks = self.split_into_sentences(text)
        elif split_by == 'paragraphs':
            chunks = self.split_into_paragraphs(text)
        else:
            raise ValueError(f"Unknown split method: {split_by}")
        
        if not chunks:
            raise ValueError("No text chunks to process")
        
        # Assign characters in rotation
        dialogue_script = []
        for idx, chunk in enumerate(chunks):
            char_idx = idx % len(characters)
            character = characters[char_idx]
            dialogue_script.append((character, chunk))
        
        return dialogue_script
