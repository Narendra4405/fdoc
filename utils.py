import google.generativeai as genai
from django.conf import settings
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import io
import openpyxl


# Configure Gemini
MODEL_NAME = "gemini-2.0-flash"
model = genai.GenerativeModel(MODEL_NAME)

def read_document_content(uploaded_file):
    """
    Read content from uploaded file based on file type
    """
    try:
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        
        file_name = uploaded_file.name.lower()
        content = ""
        
        if file_name.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
        
        elif file_name.endswith('.pdf'):
            # Create a BytesIO object from the uploaded file
            pdf_file = io.BytesIO(uploaded_file.read())
            pdf_reader = PdfReader(pdf_file)
            
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
        
        elif file_name.endswith('.docx'):
            # Create a BytesIO object from the uploaded file
            docx_file = io.BytesIO(uploaded_file.read())
            doc = DocxDocument(docx_file)
            
        elif file_name.endswith('.xlsx'):

            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
        
        else:
            return None
            
        return content.strip()
        
    except Exception as e:
        print(f"Error reading document: {e}")
        return None

def ask_gemini(document_content, user_question):
    """
    Send question to Gemini AI with document content
    """
    prompt_parts = [
        "You are a helpful document assistant. If the document contains photo then explain about the photo. Based on the content of the document provided, answer the user's question. You can convert any document into any language asked by the user.",
        "Document Content:\n" + document_content,
        "User Question:\n" + user_question,
    ]
    
    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        print(f"Error communicating with Gemini: {e}")
        return "Sorry, I encountered an error while processing your question."