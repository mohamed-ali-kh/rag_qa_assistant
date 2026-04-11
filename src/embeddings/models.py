from langchain_cohere import CohereEmbeddings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def create_embedding_model():
    return CohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=os.getenv("COHERE_API_KEY")
    )