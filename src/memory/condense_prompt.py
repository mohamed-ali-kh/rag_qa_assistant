from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

condense_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """rephrase the next follow up questions into a standalone question.
        if there is no chat history return the question as it is."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ]
)