import streamlit as st
from langchain_core.messages import HumanMessage
from core.graph import graph
from core.config import init_app, get_flattened_languages

# Initialize App
init_app("Multi-Lang AI Assistant", "🌐")

all_languages = get_flattened_languages()

# Initialize App
init_app("Multi-Lang AI Assistant", "🌐")

all_languages = get_flattened_languages()

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    intelligence_rating = st.selectbox(
        "Intelligence Rating",
        options=["Ultra", "High", "Medium", "Low"],
        index=1,
        help="Ultra: Gemini 3 | High: Gemini 3.1 Lite | Medium: Llama 4 Scout | Low: Llama 3.3 70B"
    )
    

# Main UI

tab1, tab2, tab3 = st.tabs([
    "🌐 Translation", 
    "✨ Grammar & Tone", 
    "📝 Drafting"
])

# Utility for running the graph
def run_assistant(input_text, task, target_lang=None, task_subtype=None):
    initial_state = {
        "messages": [HumanMessage(content=input_text)],
        "task": task,
        "intelligence_rating": intelligence_rating,
        "target_lang": target_lang,
        "task_subtype": task_subtype
    }
    
    with st.spinner(f"Agent is working on {task}..."):
        result = graph.invoke(initial_state)
        return result

# Tab 1: Translation
with tab1:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📥 Input")
        source_text = st.text_area("Source Text", placeholder="Enter text to translate...", height=250, key="trans_src")
        target_lang = st.selectbox(
            "Target Language", 
            options=all_languages,
            index=all_languages.index("English") if "English" in all_languages else 0
        )
        
    with col2:
        st.markdown("### 📤 Output")
        if st.button("🚀 Run Translation", key="btn_trans"):
            if source_text:
                result = run_assistant(source_text, "translate", target_lang=target_lang)
                st.success(result["output"])
            else:
                st.warning("Please provide text to translate.")

# Tab 2: Grammar & Tone
with tab2:
    col_g1, col_g2 = st.columns(2, gap="large")
    with col_g1:
        st.markdown("### 📝 Input")
        edit_text = st.text_area("Text to Refine", placeholder="Paste your text here...", height=250, key="edit_src")
    
    with col_g2:
        st.markdown("### ✨ Results")
        if st.button("✨ Improve Text", key="btn_edit"):
            if edit_text:
                result = run_assistant(edit_text, "grammar")
                
                output = result["output"]
                metadata = result.get("metadata", {})
                
                st.markdown("#### ✅ Corrected Text")
                st.success(output)
                
                if metadata and "explanation" in metadata:
                    st.markdown("#### 💡 Explanation")
                    st.info(metadata["explanation"])
            else:
                st.warning("Please provide text to refine.")

# Tab 3: Drafting
with tab3:
    col_d1, col_d2 = st.columns(2, gap="large")
    
    with col_d1:
        st.markdown("### 🛠 Options")
        draft_type = st.radio("Type", ["Email", "Document", "Research", "Custom"], horizontal=True)
        instructions = st.text_area("Instructions/Notes", placeholder="Explain what needs to be drafted...", height=200)
        
    with col_d2:
        st.markdown("### 📄 Draft")
        if st.button("✍️ Generate", key="btn_draft"):
            if instructions:
                result = run_assistant(instructions, "draft", task_subtype=draft_type.lower())
                st.markdown(result["output"])
            else:
                st.warning("Please provide instructions.")

