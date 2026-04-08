import os
from langchain_groq import ChatGroq


def get_llm(model: str = "llama-3.3-70b-versatile", temperature: float = 0.2) -> ChatGroq:
    """
    Returns a ChatGroq instance.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if api_key :
        return ChatGroq(model=model, temperature=temperature, groq_api_key=api_key)