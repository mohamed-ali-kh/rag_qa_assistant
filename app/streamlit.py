import streamlit as st
from src.rag.chain import chain


st.title("RAG Chatbot")

# 1. Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Function to clear input after submission
def submit():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ""

# 3. Sidebar for configuration
with st.sidebar:
    session_id = st.text_input("Session ID", value="default_user")
    config = {"configurable": {"session_id": session_id}}
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        # Optional: Add logic to clear the 'store' in pipeline.py if needed

# 4. Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input
if prompt := st.chat_input("Ask something..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 6. Generate Response
    # 6. Generate Response
    with st.chat_message("assistant"):
        # We call .stream instead of .invoke
        # This returns a generator (the object you saw in your error)
        response_generator = chain.stream({"question": prompt}, config=config)
    
        # st.write_stream automatically iterates through the generator 
        # and displays it piece-by-piece on the screen
        full_response = st.write_stream(response_generator)

    # Add the final string to your session state history
    st.session_state.messages.append({"role": "assistant", "content": full_response})