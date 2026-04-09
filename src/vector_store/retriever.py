from src.vector_store.hybrid_retriever import get_hybrid_retriever

def get_retriever():
    return get_hybrid_retriever(r"data\faiss_index")
