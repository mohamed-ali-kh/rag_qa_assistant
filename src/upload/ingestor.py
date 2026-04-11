from src.upload.create_user_dir import get_user_dir
from src.ingestion.loader import SUPPORTED_FILE_TYPES
from src.embeddings.models import create_embedding_model
from src.embeddings.embedder import embed_chunks
from src.vector_store.hybrid_retriever import get_hybrid_retriever
from langchain_community.vectorstores import FAISS
import os


def ingest_uploaded_file(filename, file_bytes , session_id):
    filename = filename.strip()
    document_dir, index_dir = get_user_dir(session_id)

    # validate extension before doing anything
    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"Unsupported file type: {ext}")

    # 1. Save raw file to disk
    file_path = os.path.join(document_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # 2. Run full pipeline — returns a FAISS store directly
    print(f"DEBUG: filename={filename}, type={type(filename)}")
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


def get_user_retriever(session_id):
    _, index_dir = get_user_dir(session_id)
    index_file = os.path.join(index_dir, "index.faiss")

    if not os.path.exists(index_file):
        return None

    return get_hybrid_retriever(index_dir)


def get_user_files(session_id):
    docs_dir, _ = get_user_dir(session_id)
    return os.listdir(docs_dir)