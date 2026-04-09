from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.vectorstores import FAISS
from src.embeddings.models import create_embedding_model
import os

def get_hybrid_retriever(index_dir):
    """
    Builds a hybrid retriever combining BM25 (keyword) and FAISS (semantic).
    index_dir: path to the user's or default faiss_index folder.
    """

    # 1- load FAISS for semantic search
    embedding_model = create_embedding_model()
    vector_store = FAISS.load_local(index_dir,
                                    embedding_model,
                                    allow_dangerous_deserialization=True)


    faiss_retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
                        "k": 5,
                        "fetch_k": 20,
                        "lambda_mult": 0.7
                        }
        )
    

    # 2- build BM25 retriever for keyword search
    docs  = list(vector_store.__dict.values())   #vector_store.docstore._dict is FAISS's internal document store — a plain Python dict where the keys are chunk IDs and the values are the actual Document objects (the text chunks + metadata). Calling .values() gives you all the documents, and wrapping it in list() converts it to a list.
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = 5

    hybrid_retriever = EnsembleRetriever(
        retrievers=[faiss_retriever, bm25_retriever],
        weights=[0.6, 0.4]  # Adjust weights as needed
    )
    return hybrid_retriever

