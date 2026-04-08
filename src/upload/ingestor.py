from src.upload.create_user_dir import get_user_dir
from src.ingestion.pipeline import run_ingestion_pipeline 
from src.embeddings.models import create_embedding_model
from src.embeddings.embedder import embed_chunks
from langchain_community.vectorstores import FAISS
from src.embeddings.embedder import embed_chunks
import os

def ingest_uploaded_file(uploaded_file, session_id):
    document_dir, index_dir = get_user_dir(session_id)

    # 1. Save raw file to disk
    file_path = os.path.join(document_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # 2. Run full pipeline — returns a FAISS store directly
    new_store = embed_chunks(file_path)

    # 3. Merge into or create the user's index
    embedding_model = create_embedding_model()
    index_file = os.path.join(index_dir, "index.faiss")

    if os.path.exists(index_file):
        vector_store = FAISS.load_local(
            index_dir,
            embedding_model,
            allow_dangerous_deserialization=True
        )
        vector_store.merge_from(new_store)
    else:
        vector_store = new_store

    # 4. Persist to disk
    vector_store.save_local(index_dir)
    return vector_store