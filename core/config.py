import os
import streamlit as st
from dotenv import load_dotenv

SUPPORTED_LANGUAGES = {
    "Indian (Official)": [
        "Hindi", "English (Associate)", "Bengali", "Telugu", "Marathi", "Tamil", "Urdu", 
        "Gujarati", "Kannada", "Malayalam", "Odia (Oriya)", "Punjabi", "Assamese", "Maithili", 
        "Sanskrit", "Kashmiri", "Nepali", "Sindhi", "Konkani", "Manipuri (Meitei)", 
        "Bodo", "Dogri"
    ],
    "Europe": [
        "English", "French", "German", "Spanish", "Italian", "Dutch", "Polish", "Greek", "Russian", "Portuguese"
    ],
    "Asia": [
        "Mandarin Chinese", "Japanese", "Korean", "Thai", "Vietnamese", "Indonesian", "Arabic"
    ],
    "Africa": [
        "Swahili", "Hausa", "Yoruba", "Amharic", "Zulu", "Igbo", "Oromo", "Tigrinya", "Somali"
    ],
    "Americas": [
        "English", "Spanish", "Portuguese", "French"
    ]
}

def get_flattened_languages():
    flat_list = []
    for category, langs in SUPPORTED_LANGUAGES.items():
        flat_list.extend(langs)
    return sorted(list(set(flat_list)))

def init_app(page_title: str, page_icon: str):
    """
    Centralized initialization for all Streamlit pages.
    """
    load_dotenv()
    
    st.set_page_config(
        page_title="Translate.AI",
        page_icon="🌐",
        layout="wide"
    )

# --- Configuration Helpers ---

def get_env_bool(key: str, default: bool = False) -> bool:
    val = os.getenv(key, str(default)).lower()
    return val in ("true", "1", "yes")

# Server Config
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8005"))
API_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/process"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
