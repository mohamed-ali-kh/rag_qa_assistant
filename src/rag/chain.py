from langchain_core.runnables import RunnableWithMessageHistory
from src.memory.chain_with_standalone import chain_with_standalone
from src.memory.create_memory_store import get_session_id


chain = RunnableWithMessageHistory(
    chain_with_standalone,
    get_session_id,
    input_messages_key="question",
    history_messages_key="chat_history"
)
