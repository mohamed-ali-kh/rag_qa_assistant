import streamlit as st
import requests
import threading

API_URL = "http://localhost:8000"

# ─── Module-level dict (accessible from background threads) ──────────────────
ingestion_status = {}

# ─── Session state init ──────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ─── API helpers ─────────────────────────────────────────────────────────────

def api_get_files(session_id):
    try:
        res = requests.get(f"{API_URL}/files/{session_id}")
        return res.json().get("files", [])
    except Exception:
        return []

def api_upload_file(filename, file_bytes, session_id):
    res = requests.post(
        f"{API_URL}/upload/{session_id}",
        files={"file": (filename, file_bytes)}
    )
    if res.status_code != 200:
        raise Exception(res.json().get("detail", "Upload failed"))

def api_delete_file(filename, session_id):
    res = requests.delete(f"{API_URL}/files/{session_id}/{filename}")
    if res.status_code != 200:
        raise Exception(res.json().get("detail", "Delete failed"))

def api_clear_user(session_id):
    requests.delete(f"{API_URL}/users/{session_id}")

def api_chat_stream(question, session_id):
    with requests.post(f"{API_URL}/chat/stream", json={
        "question": question,
        "session_id": session_id
    }, stream=True) as res:
        if res.status_code != 200:
            raise Exception(res.json().get("detail", "Chat failed"))
        for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                if "__SOURCES__" in chunk:
                    parts = chunk.split("__SOURCES__")
                    if parts[0]:
                        yield parts[0], []
                    sources = parts[1].split(",") if parts[1] else []
                    yield "", sources
                else:
                    yield chunk, []


# ─── Background ingestion ────────────────────────────────────────────────────

def ingest_in_background(filename, file_bytes, session_id):
    try:
        api_upload_file(filename, file_bytes, session_id)
        ingestion_status[filename] = "done"
    except Exception as e:
        ingestion_status[filename] = f"error: {e}"


# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Settings")
    session_id = st.text_input("Session ID", value="default_user")

    st.divider()

    st.subheader("📄 Upload Documents")
    uploaded = st.file_uploader(
        "Add documents to your knowledge base",
        type=["pdf", "txt", "docx", "md"],
        accept_multiple_files=True,
    )

    if uploaded:
        already_indexed = api_get_files(session_id)
        in_progress = [k for k, v in ingestion_status.items() if v == "processing"]
        new_files = [f for f in uploaded if f.name not in already_indexed and f.name not in in_progress]

        for file in new_files:
            file_bytes = file.getvalue()
            ingestion_status[file.name] = "processing"
            thread = threading.Thread(
                target=ingest_in_background,
                args=(file.name, file_bytes, session_id),
                daemon=True
            )
            thread.start()

    # Show ingestion statuses
    for fname, status in ingestion_status.items():
        if status == "processing":
            st.caption(f"⏳ Processing {fname}...")
        elif status == "done":
            st.success(f"✅ {fname} indexed")
        elif status.startswith("error"):
            st.error(f"❌ {fname}: {status}")

    # Show indexed files with delete buttons
    existing_files = api_get_files(session_id)
    if existing_files:
        st.caption("Indexed files:")
        for fname in existing_files:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.caption(f"• {fname}")
            with col2:
                if st.button("🗑️", key=f"del_{fname}"):
                    with st.spinner(f"Removing {fname}..."):
                        try:
                            api_delete_file(fname, session_id)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {e}")

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        requests.delete(f"{API_URL}/users/{session_id}/history")
        st.rerun()

    if st.button("🗑️ Clear Uploaded Docs"):
        api_clear_user(session_id)
        ingestion_status.clear()
        st.rerun()


# ─── Chat UI ─────────────────────────────────────────────────────────────────

st.title("RAG Chatbot")

if not api_get_files(session_id):
    st.info("💡 Upload documents in the sidebar to ask questions about them.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            full_response = ""
            sources = []
            response_placeholder = st.empty()

            for chunk, chunk_sources in api_chat_stream(prompt, session_id):
                if chunk_sources:
                    sources = chunk_sources
                if chunk:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

            if sources:
                with st.expander("📚 Sources"):
                    for source in sorted(sources):
                        st.caption(f"• {source}")

        except Exception as e:
            st.error(f"❌ {e}")
            full_response = None

    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})