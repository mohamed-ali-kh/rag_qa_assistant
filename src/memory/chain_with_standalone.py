from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from .condense_prompt import condense_prompt
from .qa_prompt import qa_prompt
from ..format_docs import format_doc
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

def chain_with_standalone(retriever):
    return(
        RunnablePassthrough.assign(
            standalone = condense_prompt | llm | StrOutputParser()
        )
        | RunnablePassthrough.assign(
                context = lambda x: format_doc(retriever.invoke(x["standalone"]))
            )
            | qa_prompt
            | llm
            | StrOutputParser()
        )