import streamlit as st
from langchain_core.messages import HumanMessage
from core.graph import graph
from core.config import init_app

# Initialize App
init_app("AI Chatbot", "💬")

st.title("💬 AI Chatbot")
st.markdown("---")

# Get intelligence rating from session state or default
if "intelligence_rating" not in st.session_state:
    st.session_state["intelligence_rating"] = "Medium"

with st.sidebar:
    st.title("⚙️ Settings")
    st.session_state["intelligence_rating"] = st.selectbox(
        "Intelligence Rating",
        options=["Ultra", "High", "Medium", "Low"],
        index=["Ultra", "High", "Medium", "Low"].index(st.session_state["intelligence_rating"]),
        help="Ultra: Gemini 3 | High: Gemini 3.1 Lite | Medium: Llama 4 Scout | Low: Llama 3.3 70B"
    )

# Chat Logic
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display history
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state["chat_history"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_msgs = [HumanMessage(content=m["content"]) for m in st.session_state["chat_history"]]
            initial_state = {
                "messages": full_msgs,
                "task": "chat",
                "intelligence_rating": st.session_state["intelligence_rating"]
            }
            res = graph.invoke(initial_state)
            st.markdown(res["output"])
            st.session_state["chat_history"].append({"role": "assistant", "content": res["output"]})
