from .models import create_embedding_model
from langchain_community.vectorstores import FAISS
from ..ingestion.pipeline import run_ingestion_pipeline

def embed_chunks(pdf_path):
    chunks = run_ingestion_pipeline(pdf_path)
    embedding_model = create_embedding_model()
    embeddings = FAISS.from_documents(chunks, embedding_model)
    return embeddings

if __name__ == "__main__":
    embed_chunks(r"data\NIPS-2017-attention-is-all-you-need-Paper.pdf")