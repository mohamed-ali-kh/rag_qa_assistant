from langchain_core.runnables import RunnableWithMessageHistory
from src.memory.chain_with_standalone import chain_with_standalone
from src.memory.create_memory_store import get_session_id
from src.upload.get_user_retriever import get_user_retriever
from src.vector_store.retriever import get_retriever





def get_chain(session_id):
    # Use the user's personal index if they've uploaded docs, otherwise fall back to the default
    retriever = get_user_retriever(session_id) or get_retriever()
    chain = RunnableWithMessageHistory(

    chain_with_standalone(retriever),
    get_session_id,
    input_messages_key="question",
    history_messages_key="chat_history"
)
    
    return chain