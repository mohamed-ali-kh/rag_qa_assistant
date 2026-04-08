from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from io import BytesIO
from pypdf import PdfReader

def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    return loader.load()
