from langchain_core.runnables import RunnableWithMessageHistory
from src.memory.chain_with_standalone import build_chain
from src.memory.create_memory_store import get_session_history
from src.upload.ingestor import get_user_retriever
from src.vector_store.retriever import get_retriever


def get_chain(session_id):
    retriever = get_user_retriever(session_id) or get_retriever()
    chain = RunnableWithMessageHistory(
        build_chain(retriever),
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
        output_messages_key="answer"        # ← tell it which key is the actual answer
    )
    return chain