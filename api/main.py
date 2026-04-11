from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from isort import file
from pydantic import BaseModel
import asyncio
import traceback


from src.rag.chain import get_chain
from src.upload.ingestor import ingest_uploaded_file
from src.upload.get_user_files import get_user_files
from src.upload.clear_user_data import clear_user_data 
from src.upload.delete_user_files import delete_user_file

from src.memory.create_memory_store import clear_session_history

app = FastAPI(title="RAG QA Assistant")


# ─── Health check ────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


# ─── Upload ──────────────────────────────────────────────────────────────────

@app.post("/upload/{session_id}")
async def upload_file(session_id: str, file: UploadFile = File(...)):
    supported = [".pdf", ".txt", ".docx", ".md"]
    ext = "." + file.filename.split(".")[-1].lower()

    if ext not in supported:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    try:
        ingest_uploaded_file(file.filename, contents, session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"message": f"{file.filename} indexed successfully"}


# ─── List files ──────────────────────────────────────────────────────────────

@app.get("/files/{session_id}")
def list_files(session_id: str):
    return {"files": get_user_files(session_id)}


# ─── Delete file ─────────────────────────────────────────────────────────────

@app.delete("/files/{session_id}/{filename}")
def delete_file(session_id: str, filename: str):
    try:
        delete_user_file(filename, session_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": f"{filename} deleted successfully"}


# ─── Clear all user data ─────────────────────────────────────────────────────

@app.delete("/users/{session_id}")
def clear_user(session_id: str):
    clear_user_data(session_id)
    clear_session_history(session_id)
    return {"message": f"User {session_id} data cleared"}


# ─── Chat ─────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str
    session_id: str

# ─── Stream chat ──────────────────────────────────────────────────────────────

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    chain = get_chain(request.session_id)

    if chain is None:
        raise HTTPException(status_code=400, detail="No documents uploaded yet.")

    config = {"configurable": {"session_id": request.session_id}}

    async def generate():
        for chunk in chain.stream({"question": request.question}, config=config):
            if "answer" in chunk:
                yield chunk["answer"]

    return StreamingResponse(generate(), media_type="text/plain")


# ─── clear chat history ──────────────────────────────────────────────────────────────
@app.delete("/users/{session_id}/history")
def clear_history(session_id: str):
    clear_session_history(session_id)
    return {"message": f"Chat history cleared for {session_id}"}