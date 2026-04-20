import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm(rating: str):
    """
    Returns the appropriate LLM based on a 4-tier intelligence system.
    Ultra:  Gemini 2.0 Flash (best multilingual, vision, and reasoning)
    High:   Gemini 1.5 Flash (fast, multilingual)
    Medium: Llama 3.3 70B (Groq)
    Low:    Llama 3.1 8B Instant (Groq - fast)
    """
    rating = rating.lower()

    if rating == "ultra":
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

    elif rating == "high":
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

    elif rating == "medium":
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

    else:
        # Low: llama-3.1-8b-instant for speed
        return ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
