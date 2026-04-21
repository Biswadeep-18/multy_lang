import streamlit as st
import requests
from langchain_core.messages import HumanMessage
from core.config import init_app, get_flattened_languages, API_URL
from core.graph import graph
from core.vision import process_uploaded_file
from core.export import generate_pdf, generate_txt

# Initialize App
init_app("Translate.AI", "🌐")

all_languages = get_flattened_languages()
# API_URL is now imported from core.config

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
        index=3,
        help="Select model intelligence level. Low uses Llama 3.3 70B."
    )
    
    st.divider()
    st.markdown("### 📄 Document Intelligence")
    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_file:
        if st.button("Extract & Sync Text", use_container_width=True, type="secondary"):
            with st.spinner("Processing document..."):
                extracted_text = process_uploaded_file(uploaded_file)
                if extracted_text:
                    # Sync to the current navigation's input key
                    if navigation == "Translate":
                        st.session_state["studio_trans_input"] = extracted_text
                    elif navigation == "Grammar and Tone":
                        st.session_state["edit_src"] = extracted_text
                    elif navigation == "Drafting":
                        st.session_state["draft_input_manual"] = extracted_text 
                    
                    # Also sync to the sub-mode in Translate if it's currently on Enterprise Draft
                    if navigation == "Translate" and st.session_state.get("trans_sub_mode") == "Enterprise Draft":
                         st.session_state["studio_draft_input_manual"] = extracted_text
                         
                    st.success("Text extracted and synced!")
                else:
                    st.warning("No text found in document.")

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
    
    # Try API Call first (Best for Structured Logs/Swagger)
    try:
        with st.spinner(f"AI System is processing {task}..."):
            response = requests.post(API_URL, json=payload, timeout=45)
            response.raise_for_status()
            res = response.json()
            if res and isinstance(res, dict) and "output" in res:
                return res
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # Fallback to Direct Graph Execution (Essential for Streamlit Cloud)
        with st.status("Backend API Offline. Running Local AI Core Fallback...", expanded=False) as status:
            try:
                initial_state = {
                    "messages": [HumanMessage(content=input_text)],
                    "task": task,
                    "intelligence_rating": intelligence_rating,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "task_subtype": task_subtype
                }
                result = graph.invoke(initial_state)
                status.update(label="AI Core Processing Complete!", state="complete", expanded=False)
                return {
                    "output": result["output"],
                    "metadata": result.get("metadata", {}),
                    "task": task
                }
            except Exception as direct_e:
                st.error(f"Integrated Engine Error: {str(direct_e)}")
                return None
    except Exception as e:
        st.error(f"Processing Error: {str(e)}")
        return None
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
            studio_input = st.text_area("Input Text", value=st.session_state.get("studio_trans_input", ""), placeholder="Enter content to translate...", height=350, key="studio_trans_input_box", label_visibility="collapsed")
            # Update the source state manually since we are using a 'value' and a dynamic key
            if studio_input != st.session_state.get("studio_trans_input"):
                st.session_state["studio_trans_input"] = studio_input
                
            if st.button("Process Translation", type="primary", use_container_width=True, key="studio_trans_btn"):
                if studio_input:
                    with st.spinner("Processing..."):
                        res = run_assistant(studio_input, "translate", target_lang=to_lang, source_lang=from_lang)
                        if res:
                            st.session_state["studio_trans_output"] = res["output"]
                            st.session_state["studio_trans_meta"] = res.get("metadata", {})
                        else:
                            st.error("Failed to get response from AI System.")
                else:
                    st.warning("Input required.")
        
        with io_col2:
            st.markdown("### Output")
            with st.container(border=True):
                if "studio_trans_output" in st.session_state:
                    if from_lang == "Detect Language" and "studio_trans_meta" in st.session_state:
                         pass # Removed caption as requested
                    st.markdown(st.session_state["studio_trans_output"])
                    
                    # Download Section
                    st.divider()
                    d_col1, d_col2 = st.columns(2)
                    with d_col1:
                        st.download_button("Download TXT", data=generate_txt(st.session_state["studio_trans_output"]), file_name="translation.txt", mime="text/plain", use_container_width=True)
                    with d_col2:
                        try:
                            pdf_bytes = generate_pdf(st.session_state["studio_trans_output"], title="Translation")
                            st.download_button("Download PDF", data=pdf_bytes, file_name="translation.pdf", mime="application/pdf", use_container_width=True)
                        except:
                            st.caption("PDF Export limited for regional scripts.")
                else:
                    st.info("Translation result will appear here.")
    else:
        draft_lang = st.selectbox("Target Language", options=all_languages, index=all_languages.index("English") if "English" in all_languages else 0, key="studio_draft_lang")
        io_col1, io_col2 = st.columns(2, gap="medium")
        with io_col1:
            st.markdown("### Draft Specifications")
            draft_input = st.text_area("Requirements", value=st.session_state.get("studio_draft_input_manual", ""), placeholder="Describe the content structure...", height=350, key="studio_draft_input", label_visibility="collapsed")
            if draft_input != st.session_state.get("studio_draft_input_manual"):
                st.session_state["studio_draft_input_manual"] = draft_input
                
            if st.button("Generate Content", type="primary", use_container_width=True, key="studio_draft_btn"):
                if draft_input:
                    with st.spinner("Generating..."):
                        res = run_assistant(draft_input, "draft", target_lang=draft_lang)
                        if res:
                            st.session_state["studio_draft_output"] = res["output"]
                        else:
                            st.error("Failed to get response from AI System.")
                else:
                    st.warning("Requirements required.")
        
        with io_col2:
            st.markdown("### Generated Draft")
            with st.container(border=True):
                if "studio_draft_output" in st.session_state:
                    st.markdown(st.session_state["studio_draft_output"])
                    
                    # Download Section
                    st.divider()
                    dd_col1, dd_col2 = st.columns(2)
                    with dd_col1:
                        st.download_button("Download TXT", data=generate_txt(st.session_state["studio_draft_output"]), file_name="draft.txt", mime="text/plain", use_container_width=True)
                    with dd_col2:
                         try:
                            pdf_bytes = generate_pdf(st.session_state["studio_draft_output"], title="Enterprise Draft")
                            st.download_button("Download PDF", data=pdf_bytes, file_name="draft.pdf", mime="application/pdf", use_container_width=True)
                         except:
                            st.caption("PDF Export limited for regional scripts.")
                else:
                    st.info("Document draft will be displayed here.")

elif navigation == "Grammar and Tone":
    col_g1, col_g2 = st.columns(2, gap="large")
    with col_g1:
        st.markdown("### Original Text")
        edit_text = st.text_area("Content to Optimize", value=st.session_state.get("edit_src", ""), placeholder="Paste your text here...", height=350, key="edit_src_box", label_visibility="collapsed")
        # Sync state
        if edit_text != st.session_state.get("edit_src"):
            st.session_state["edit_src"] = edit_text
            
        if st.button("Optimize Content", key="btn_edit", type="primary", use_container_width=True):
            if edit_text:
                # Access grammar_lang defined in col_g2
                target_lang = st.session_state.get("grammar_lang", "English")
                result = run_assistant(edit_text, "grammar", target_lang=target_lang)
                if result:
                    st.session_state["grammar_output"] = result["output"]
                    st.session_state["grammar_meta"] = result.get("metadata", {})
                else:
                    st.error("Failed to optimize content.")
            else:
                st.warning("Content required.")
    
    with col_g2:
        st.markdown("### Refined Version")
        grammar_lang = st.selectbox("Language", options=all_languages, index=all_languages.index("English") if "English" in all_languages else 0, key="grammar_lang")
        
        if "grammar_output" in st.session_state:
            st.success(st.session_state["grammar_output"])
            if "grammar_meta" in st.session_state and "explanation" in st.session_state["grammar_meta"]:
                st.markdown("#### Revision Intelligence")
                st.info(st.session_state["grammar_meta"]["explanation"])
            
            # Download Section
            st.divider()
            dg_col1, dg_col2 = st.columns(2)
            with dg_col1:
                st.download_button("Download TXT", data=generate_txt(st.session_state["grammar_output"]), file_name="refined_text.txt", mime="text/plain", use_container_width=True)
            with dg_col2:
                try:
                    pdf_bytes = generate_pdf(st.session_state["grammar_output"], title="Grammar Refinement")
                    st.download_button("Download PDF", data=pdf_bytes, file_name="grammar.pdf", mime="application/pdf", use_container_width=True)
                except:
                    st.caption("PDF Export limited for regional scripts.")
        else:
            st.info("The refined version will appear here.")

elif navigation == "Drafting":
    col_d1, col_d2 = st.columns(2, gap="large")
    
    with col_d1:
        st.markdown("### Specifications")
        draft_type = st.radio("Document Type", ["Email", "Document", "Research", "Custom"], horizontal=True)
        instructions = st.text_area("Prompt", value=st.session_state.get("draft_input_manual", ""), placeholder="Detailed instructions for the AI...", height=350, key="draft_input_box", label_visibility="collapsed")
        # Sync state
        if instructions != st.session_state.get("draft_input_manual"):
            st.session_state["draft_input_manual"] = instructions
            
        if st.button("Execute Draft", key="btn_draft", type="primary", use_container_width=True):
            if instructions:
                # Need to access draft_target_lang which is defined in col_d2
                # In Streamlit, we can just use the key if it's already rendered or will be
                result = run_assistant(instructions, "draft", task_subtype=draft_type.lower(), target_lang=st.session_state.get("draft_target_lang", "English"))
                if result:
                    st.session_state["pure_draft_output"] = result["output"]
                else:
                    st.error("Failed to generate document.")
            else:
                st.warning("Prompt required.")
        
    with col_d2:
        st.markdown("### Resulting Document")
        # Move selector here
        draft_target_lang = st.selectbox("Output Language", options=all_languages, index=all_languages.index("English") if "English" in all_languages else 0, key="draft_target_lang")
        
        if "pure_draft_output" in st.session_state:
            st.markdown(st.session_state["pure_draft_output"])
            
            # Download Section
            st.divider()
            dr_col1, dr_col2 = st.columns(2)
            with dr_col1:
                st.download_button("Download TXT", data=generate_txt(st.session_state["pure_draft_output"]), file_name="document.txt", mime="text/plain", use_container_width=True)
            with dr_col2:
                try:
                    pdf_bytes = generate_pdf(st.session_state["pure_draft_output"], title="Generated Document")
                    st.download_button("Download PDF", data=pdf_bytes, file_name="document.pdf", mime="application/pdf", use_container_width=True)
                except:
                    st.caption("PDF Export limited for regional scripts.")
        else:
            st.info("The generated document will appear here.")
