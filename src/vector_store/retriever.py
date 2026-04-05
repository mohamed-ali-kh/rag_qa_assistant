from langchain_community.vectorstores import FAISS
from ..embeddings.models import create_embedding_model


def get_retriever():
    embedding_model = create_embedding_model()
    vector_store = FAISS.load_local(
                                    r"data\faiss_index",
                                    embedding_model,
                                    allow_dangerous_deserialization=True
                                    )
    
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6, "lambda_mult": 0.7}
    )
