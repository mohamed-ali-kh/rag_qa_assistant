# rag_qa_assistant
A conversational AI assistant built with LangChain and Streamlit that uses Retrieval-Augmented Generation (RAG) to answer questions based on your custom documents.

# features
-Document Retrieval: Context-aware answers based on your uploaded PDFs/docs.
-Streaming UI: Real-time word-by-word response generation for a smooth user experience.
-Memory: remembers conversations 

# Setup & Installation

1. Clone the repository
git clone https://github.com/mohamed-ali-kh/rag_qa_assistant.git
cd rag_qa_assistant

2. Install Dependencies
pip install -r requirements.txt

3. Environment Variables
Create a .env file and add your API keys

4.Get your API keys:
Groq (free): https://console.groq.com
Cohere (free tier): https://cohere.com

5. Start Redis
docker run -d -p 6379:6379 --name redis redis
Or install Redis natively on your machine.

6. Start the FastAPI backend
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

7. Start the Streamlit frontend
streamlit run app/stream.py


#  How It Works
Document Ingestion

User uploads a file via the sidebar
File is saved to users_data/users/{session_id}/documents/
Document is loaded, split into chunks (600 tokens, 100 overlap)
Chunks are embedded using Cohere's embed-english-v3.0 model
FAISS index is built/updated and saved to users_data/users/{session_id}/faiss_index/

Retrieval & Answering

User's question is condensed into a standalone question using chat history
Hybrid retriever fetches top 10 candidates from both BM25 and FAISS (MMR)
Flashrank reranker scores all candidates and returns the best 6
LLM (LLaMA 3.3 70B via Groq) generates an answer using the retrieved context
Answer streams back to the UI with source attribution

Memory

Recent messages (last 4 turns) are kept in full
Older messages are summarized into a single system message
All history is persisted in Redis with a 24-hour TTL


