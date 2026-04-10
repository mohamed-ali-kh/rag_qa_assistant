#from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_redis import RedisChatMessageHistory
import  os 
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

"""store = {}  # wiped on every restart
def get_session_id(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]"""

def get_session_history(session_id):
    return RedisChatMessageHistory(
        session_id=session_id,
        redis_url=REDIS_URL,
        ttl=60 * 60 * 24  # 1 day
    )

def clear_session_history(session_id):
    history = get_session_history(session_id)
    history.clear()