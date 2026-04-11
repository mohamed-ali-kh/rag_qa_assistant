from src.upload.create_user_dir import get_user_dir
from src.embeddings.models import create_embedding_model
from src.embeddings.embedder import embed_chunks
import os
import shutil


def delete_user_file(file_name, session_id):
    doc_dir, index_dir = get_user_dir(session_id)
    file_path = os.path.join(doc_dir, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f" {file_name} not found")
    os.remove(file_path)

    remaining_files = os.listdir(doc_dir)
    if not remaining_files:
        # If no files left, remove the index too
        shutil.rmtree(index_dir)
        os.makedirs(index_dir, exist_ok=True)
        return
    
    vector_store = None
    embedding_model = create_embedding_model()
    for file_name in remaining_files:
        file_path = os.path.join(doc_dir, file_name)
        new_vector_store = embed_chunks(file_path)
        if vector_store is None:
            vector_store = new_vector_store
        else:
            vector_store.merge_from(new_vector_store)
        
    vector_store.save_local(index_dir)
