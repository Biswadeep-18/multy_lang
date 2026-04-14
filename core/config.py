import streamlit as st
from dotenv import load_dotenv

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
