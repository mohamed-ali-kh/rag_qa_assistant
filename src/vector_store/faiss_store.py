from ..embeddings.embedder import embed_chunks

def create_vector_store():
    pdf_path = r"data\NIPS-2017-attention-is-all-you-need-Paper.pdf"
    vector_store = embed_chunks(pdf_path)
    vector_store.save_local("data/faiss_index")
    return vector_store

if __name__ == "__main__":
    create_vector_store()
    print("Vector store created successfully!")





