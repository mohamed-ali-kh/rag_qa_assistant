from src.upload.create_user_dir import get_user_dir
from src.embeddings.models import create_embedding_model
from langchain_community.vectorstores import FAISS
import os

def get_user_retriever(session_id):
    _, vector_store_dir = get_user_dir(session_id)
    if not os.path.exists(vector_store_dir):
        return None
    
    embedding_model = create_embedding_model()
    vector_store = FAISS.load_local(
        vector_store_dir,
        embedding_model,
        allow_dangerous_deserialization=True
    )
    return vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 6,
                "lambda_mult": 0.7,
                "fetch_k": 20
                
                }
    )
