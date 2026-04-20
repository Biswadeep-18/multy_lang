import streamlit as st
import requests
from core.config import init_app, get_flattened_languages

# Initialize App
init_app("Translate.AI", "🌐")

all_languages = get_flattened_languages()
API_URL = "http://localhost:8000/process"

# Sidebar Navigation
with st.sidebar:
    st.title("Translate.AI")
    
    navigation = st.radio(
        "Navigation",
        options=["Translate", "Grammar and Tone", "Drafting"],
        index=0
    )
    
    st.divider()
    st.markdown("### Configuration")
    intelligence_rating = st.selectbox(
        "Intelligence Rating",
        options=["Ultra", "High", "Medium", "Low"],
        index=1,
        help="Elite Models for Production Use"
    )

# Utility for running the backend controller
def run_assistant(input_text, task, target_lang=None, source_lang=None, task_subtype=None):
    payload = {
        "text": input_text,
        "task": task,
        "intelligence_rating": intelligence_rating,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "task_subtype": task_subtype
    }
    
    try:
        with st.spinner(f"AI System is processing {task}..."):
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Backend Server Error: Connection Refused. Please ensure the FastAPI server is running.")
        return None
    except Exception as e:
        st.error(f"Processing Error: {str(e)}")
        return None

# --- Main UI Logic ---

if navigation == "Translate":
    sub_mode = st.radio("Translation Sub-mode", ["Standard Translate", "Enterprise Draft"], horizontal=True, label_visibility="hidden", key="trans_sub_mode")
    
    st.divider()
    
    if sub_mode == "Standard Translate":
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            from_lang = st.selectbox("Source Language", options=["Detect Language"] + all_languages, key="studio_from_lang")
        with lang_col2:
            to_lang = st.selectbox("Target Language", options=all_languages, index=all_languages.index("English") if "English" in all_languages else 0, key="studio_to_lang")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        io_col1, io_col2 = st.columns(2, gap="medium")
        with io_col1:
            st.markdown("### Input")
            studio_input = st.text_area("Input Text", placeholder="Enter content to translate...", height=350, key="studio_trans_input", label_visibility="collapsed")
            if st.button("Process Translation", type="primary", use_container_width=True, key="studio_trans_btn"):
                if studio_input:
                    with st.spinner("Processing..."):
                        res = run_assistant(studio_input, "translate", target_lang=to_lang, source_lang=from_lang)
                        st.session_state["studio_trans_output"] = res["output"]
                        st.session_state["studio_trans_meta"] = res.get("metadata", {})
                else:
                    st.warning("Input required.")
        
        with io_col2:
            st.markdown("### Output")
            with st.container(border=True):
                if "studio_trans_output" in st.session_state:
                    if from_lang == "Detect Language" and "studio_trans_meta" in st.session_state:
                         detected = st.session_state["studio_trans_meta"].get("detected_language", "Unknown")
                         st.caption(f"Language Identification: {detected}")
                    st.markdown(st.session_state["studio_trans_output"])
                else:
                    st.info("Translation result will appear here.")
    else:
        draft_lang = st.selectbox("Target Language", options=all_languages, index=all_languages.index("English") if "English" in all_languages else 0, key="studio_draft_lang")
        io_col1, io_col2 = st.columns(2, gap="medium")
        with io_col1:
            st.markdown("### Draft Specifications")
            draft_input = st.text_area("Requirements", placeholder="Describe the content structure...", height=350, key="studio_draft_input", label_visibility="collapsed")
            if st.button("Generate Content", type="primary", use_container_width=True, key="studio_draft_btn"):
                if draft_input:
                    with st.spinner("Generating..."):
                        res = run_assistant(draft_input, "draft", target_lang=draft_lang)
                        st.session_state["studio_draft_output"] = res["output"]
                else:
                    st.warning("Requirements required.")
        
        with io_col2:
            st.markdown("### Generated Draft")
            with st.container(border=True):
                if "studio_draft_output" in st.session_state:
                    st.markdown(st.session_state["studio_draft_output"])
                else:
                    st.info("Document draft will be displayed here.")

elif navigation == "Grammar and Tone":
    col_g1, col_g2 = st.columns(2, gap="large")
    with col_g1:
        st.markdown("### Original Text")
        edit_text = st.text_area("Content to Optimize", placeholder="Paste your text here...", height=350, key="edit_src", label_visibility="collapsed")
        if st.button("Optimize Content", key="btn_edit", type="primary", use_container_width=True):
            if edit_text:
                result = run_assistant(edit_text, "grammar")
                st.session_state["grammar_output"] = result["output"]
                st.session_state["grammar_meta"] = result.get("metadata", {})
            else:
                st.warning("Content required.")
    
    with col_g2:
        st.markdown("### Refined Version")
        if "grammar_output" in st.session_state:
            st.success(st.session_state["grammar_output"])
            if "grammar_meta" in st.session_state and "explanation" in st.session_state["grammar_meta"]:
                st.markdown("#### Revision Intelligence")
                st.info(st.session_state["grammar_meta"]["explanation"])
        else:
            st.container(border=True).write("The refined version will appear here.")

elif navigation == "Drafting":
    col_d1, col_d2 = st.columns(2, gap="large")
    
    with col_d1:
        st.markdown("### Specifications")
        draft_type = st.radio("Document Type", ["Email", "Document", "Research", "Custom"], horizontal=True)
        instructions = st.text_area("Prompt", placeholder="Detailed instructions for the AI...", height=300, label_visibility="collapsed")
        if st.button("Execute Draft", key="btn_draft", type="primary", use_container_width=True):
            if instructions:
                result = run_assistant(instructions, "draft", task_subtype=draft_type.lower())
                st.session_state["pure_draft_output"] = result["output"]
            else:
                st.warning("Prompt required.")
        
    with col_d2:
        st.markdown("### Resulting Document")
        if "pure_draft_output" in st.session_state:
            st.markdown(st.session_state["pure_draft_output"])
        else:
            st.container(border=True).write("The generated document will appear here.")
