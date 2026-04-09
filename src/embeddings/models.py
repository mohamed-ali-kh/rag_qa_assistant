from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings


@lru_cache(maxsize=1)   #@lru_cache(maxsize=1) means the model is loaded once and reused everywhere
def create_embedding_model():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model