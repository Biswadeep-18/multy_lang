import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm(rating: str):
    """
    Returns the appropriate LLM based on a 4-tier intelligence system.
    Ultra:  Gemini 3 Flash Preview
    High:   Gemini 3.1 Flash Lite Preview
    Medium: Llama 4 Scout 17B (Groq)
    Low:    Llama 3.3 70B (Groq)
    """
    rating = rating.lower()
    
    if rating == "ultra":
        # Ultra: gemini-3-flash-preview
        return ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=1.0)
    
    elif rating == "high":
        # High: gemini-3.1-flash-lite-preview
        return ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=1.0)
    
    elif rating == "medium":
        # Medium: Llama 3.1 70B
        return ChatGroq(model="llama-3.1-70b-versatile", temperature=0.7)
    
    else:
        # Low: Llama 3.3 70B
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
