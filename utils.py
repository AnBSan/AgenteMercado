from langchain.chat_models import BaseChatModel, init_chat_model
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

def load_llm() -> BaseChatModel:
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

def load_llm_ollama() -> BaseChatModel:
    return init_chat_model('ollama:llama3.2:latest')