import os
import shutil
from .create_user_dir import BASE_DIR

def clear_user_files(session_id):
    """Wipes all docs and the index for a user."""
    session_id = str(session_id)
    user_dir = os.path.join(BASE_DIR, session_id)
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)