"""
Document Parser Module
Handles extraction of text from various document formats (PDF, DOCX)
"""

import fitz  # PyMuPDF
from docx import Document
import io
from typing import Optional, Dict, Any


class DocumentParser:
    """Handles parsing of different document formats"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx']
    
    def extract_text(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Extract text from uploaded document
        
        Args:
            file_content: Raw file content as bytes
            filename: Name of the uploaded file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return self._extract_from_pdf(file_content)
        elif file_extension == 'docx':
            return self._extract_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_pdf(self, file_content: bytes) -> Dict[str, Any]:
        """
        Extract text from PDF using PyMuPDF
        
        Args:
            file_content: Raw PDF content as bytes
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Open PDF from bytes
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            
            text_content = ""
            page_count = len(pdf_document)
            
            # Extract text from each page
            for page_num in range(page_count):
                page = pdf_document[page_num]
                text_content += page.get_text()
                text_content += "\n\n"  # Add spacing between pages
            
            pdf_document.close()
            
            return {
                'text': text_content.strip(),
                'page_count': page_count,
                'format': 'PDF',
                'word_count': len(text_content.split())
            }
            
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _extract_from_docx(self, file_content: bytes) -> Dict[str, Any]:
        """
        Extract text from DOCX using python-docx
        
        Args:
            file_content: Raw DOCX content as bytes
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Open DOCX from bytes
            doc = Document(io.BytesIO(file_content))
            
            text_content = ""
            paragraph_count = 0
            
            # Extract text from paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():  # Skip empty paragraphs
                    text_content += paragraph.text + "\n"
                    paragraph_count += 1
            
            return {
                'text': text_content.strip(),
                'paragraph_count': paragraph_count,
                'format': 'DOCX',
                'word_count': len(text_content.split())
            }
            
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    def validate_file(self, filename: str, file_size: int) -> bool:
        """
        Validate uploaded file
        
        Args:
            filename: Name of the file
            file_size: Size of the file in bytes
            
        Returns:
            True if file is valid, False otherwise
        """
        # Check file extension
        file_extension = '.' + filename.lower().split('.')[-1]
        if file_extension not in self.supported_formats:
            return False
        
        # Check file size (limit to 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            return False
        
        return True
    
    def get_file_info(self, filename: str, file_size: int) -> Dict[str, Any]:
        """
        Get basic information about the uploaded file
        
        Args:
            filename: Name of the file
            file_size: Size of the file in bytes
            
        Returns:
            Dictionary with file information
        """
        file_extension = '.' + filename.lower().split('.')[-1]
        
        return {
            'filename': filename,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'format': file_extension.upper(),
            'is_valid': self.validate_file(filename, file_size)
        }
