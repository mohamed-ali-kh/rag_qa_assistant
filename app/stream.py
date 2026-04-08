import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from src.rag.chain import get_chain
from src.upload.ingestor import ingest_uploaded_file
from src.upload.get_user_files import get_user_files
from src.upload.clear_user_files import clear_user_files

# ─── Session state init ──────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Settings")
    session_id = st.text_input("Session ID", value="default_user")
    config = {"configurable": {"session_id": session_id}}

    st.divider()

    # ── Document upload ──────────────────────────────────────────────────────
    st.subheader("📄 Upload Documents")
    uploaded = st.file_uploader(
        "Add PDFs to your knowledge base",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded:
        already_indexed = get_user_files(session_id)
        new_files = [f for f in uploaded if f.name not in already_indexed]

        if new_files:
            with st.spinner(f"Processing {len(new_files)} file(s)..."):
                for file in new_files:
                    try:
                        ingest_uploaded_file(file, session_id)
                        st.success(f"✅ {file.name} indexed")
                    except Exception as e:
                        st.error(f"❌ {file.name}: {e}")

    # Show all files this user has indexed (persists across refreshes)
    existing_files = get_user_files(session_id)
    if existing_files:
        st.caption("Indexed files:")
        for name in existing_files:
            st.caption(f"• {name}")

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑️ Clear Uploaded Docs"):
        clear_user_files(session_id)
        st.success("Documents cleared.")
        st.rerun()

# ─── Chat UI ─────────────────────────────────────────────────────────────────

st.title("RAG Chatbot")

if not get_user_files(session_id):
    st.info("💡 Upload PDFs in the sidebar to ask questions about them.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        chain = get_chain(session_id)
        response_generator = chain.stream({"question": prompt}, config=config)
        full_response = st.write_stream(response_generator)

    st.session_state.messages.append({"role": "assistant", "content": full_response})