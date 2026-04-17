import os
import streamlit as st
from dotenv import load_dotenv

SUPPORTED_LANGUAGES = {
    "🌍 European": ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian"],
    "🇮🇳 Indian": ["Hindi", "Bengali", "Marathi", "Telugu", "Tamil", "Gujarati", "Urdu", "Punjabi", "Kannada", "Malayalam"],
    "🇪🇹 Ethiopian": ["Amharic", "Tigrinya", "Oromo", "Somali"],
    "🌍 African (Other)": ["Swahili", "Yoruba", "Igbo", "Hausa", "Zulu"],
    "🌏 South Asian": ["Nepali", "Sinhala", "Urdu (Pakistan)", "Pashto"]
}

def get_flattened_languages():
    flat_list = []
    for category, langs in SUPPORTED_LANGUAGES.items():
        flat_list.extend(langs)
    return sorted(flat_list)

def init_app(page_title: str, page_icon: str):
    """
    Centralized initialization for all Streamlit pages.
    """
    load_dotenv()
    
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide"
    )
