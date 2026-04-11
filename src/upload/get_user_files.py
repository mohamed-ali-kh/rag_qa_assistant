from src.upload.create_user_dir import get_user_dir
from src.upload.create_user_dir import BASE_DIR
import os

def get_user_files(session_id):
    user_dir = os.path.join(BASE_DIR, session_id)
    docs_dir = os.path.join(user_dir, "documents")
    if not os.path.exists(docs_dir):
        return []
    return os.listdir(docs_dir)


