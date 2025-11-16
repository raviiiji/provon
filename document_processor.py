import os
from docx import Document
import fitz  # PyMuPDF

class DocumentProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def process_pdf(self, file_path):
        """Extract text from PDF files using PyMuPDF"""
        text = ""
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def process_txt(self, file_path):
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    def process_docx(self, file_path):
        """Extract text from Word documents"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading Word document: {str(e)}"
    
    def process_file(self, file_path):
        """Process any supported file type"""
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
            
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return self.process_pdf(file_path)
        elif file_extension == 'txt':
            return self.process_txt(file_path)
        elif file_extension == 'docx':
            return self.process_docx(file_path)
        else:
            return f"Unsupported file type: {file_extension}"
    
    def chunk_text(self, text):
        """Simple text chunking"""
        if not text or text.startswith("Error"):
            return []
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            chunks.append(chunk)
            if i + self.chunk_size >= len(words):
                break
                
        return chunks