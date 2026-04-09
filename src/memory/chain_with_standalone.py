from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from .condense_prompt import condense_prompt
from .qa_prompt import qa_prompt
from src.format_docs import format_doc
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


def build_chain(retriever):
    def retrieve_with_sources(x):
        docs = retriever.invoke(x["standalone"])
        return {
            "context": format_doc(docs),
            "sources": list({
                f"{doc.metadata.get('source', 'Unknown')}, page {doc.metadata.get('page', '?')}"
                for doc in docs
            })
        }

    return (
        RunnablePassthrough.assign(
            standalone=condense_prompt | llm | StrOutputParser()
        )
        | RunnablePassthrough.assign(
            retrieved=retrieve_with_sources
        )
        | RunnablePassthrough.assign(
            context=lambda x: x["retrieved"]["context"],
            sources=lambda x: x["retrieved"]["sources"]
        )
        | {
            "answer": qa_prompt | llm | StrOutputParser(),
            "sources": lambda x: x["sources"]
        }
    )