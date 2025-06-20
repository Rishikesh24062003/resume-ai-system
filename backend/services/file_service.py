
import pdfplumber
from docx import Document
import re
import logging
from typing import Tuple
class FileService:
    """Service for extracting text from various file formats"""
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        """Extract text from uploaded file based on file type"""
        try:
            if file_type.lower() == 'pdf':
                return FileService._extract_from_pdf(file_path)
            elif file_type.lower() in ['docx', 'doc']:
                return FileService._extract_from_docx(file_path)
            elif file_type.lower() == 'txt':
                return FileService._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            logging.error(f"Error extracting text from {file_path}: {e}")
            raise
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logging.error(f"Error extracting PDF text: {e}")
            raise
        return FileService._clean_text(text)
    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return FileService._clean_text(text)
        except Exception as e:
            logging.error(f"Error extracting DOCX text: {e}")
            raise
    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return FileService._clean_text(text)
        except Exception as e:
            logging.error(f"Error extracting TXT text: {e}")
            raise
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep essential punctuation
        text = re.sub(r'[^\w\s@.-]', ' ', text)
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        return text.strip()
    @staticmethod
    def validate_file(filename: str, max_size: int = 5 * 1024 * 1024) -> Tuple[bool, str]:
        """Validate uploaded file"""
        if not filename:
            return False, "No filename provided"
        allowed_extensions = {'pdf', 'docx', 'doc', 'txt'}
        file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if file_extension not in allowed_extensions:
            return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        return True, "File valid"

