from langchain_community.document_loaders import (PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredMarkdownLoader)
import os




SUPPORTED_FILE_TYPES = [".pdf", ".txt", ".docx", ".md"]

def load_file(file_path):
    type = os.path.splitext(file_path)[1].lower()
    if type == ".pdf":
        return PyPDFLoader(file_path).load()
    elif type == ".txt":
        return TextLoader(file_path).load()
    elif type == ".docx":
        return Docx2txtLoader(file_path).load()
    elif type == ".md":
        return UnstructuredMarkdownLoader(file_path).load()
    else:
        raise ValueError(f"Unsupported file type: {type}. Supported: {SUPPORTED_FILE_TYPES}")

