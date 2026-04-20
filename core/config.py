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
        page_icon="🌐", # Icon is okay for browser tab, but removing from UI as requested
        layout="wide"
    )
