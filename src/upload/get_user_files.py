from src.upload.create_user_dir import get_user_dir
import os

def get_user_files(session_id):
    """Returns a list of filenames the user has uploaded."""
    docs_dir, _ = get_user_dir(session_id)
    return os.listdir(docs_dir)