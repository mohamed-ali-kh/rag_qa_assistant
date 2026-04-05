from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """answer the question using only the context below.
        if the answer isn't in the context, say 'i don't know.
        context: {context} """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ]
)