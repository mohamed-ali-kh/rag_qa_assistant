import os 

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "users_data", "users")
BASE_DIR = os.path.normpath(BASE_DIR)

def get_user_dir(session_id):
    session_id = str(session_id)
    user_dir = os.path.join(BASE_DIR, session_id)
    document_dir = os.path.join(user_dir, "documents")
    vector_store_dir = os.path.join(user_dir, "faiss_index")
    os.makedirs(document_dir, exist_ok=True)
    os.makedirs(vector_store_dir, exist_ok=True)

    return document_dir, vector_store_dir
