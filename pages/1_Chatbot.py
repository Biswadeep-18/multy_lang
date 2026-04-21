import streamlit as st
from langchain_core.messages import HumanMessage
from core.graph import graph
from core.config import init_app

# Initialize App
init_app("AI System", "")

st.title("AI Intelligence")

# Get intelligence rating from session state or default
if "intelligence_rating" not in st.session_state:
    st.session_state["intelligence_rating"] = "Medium"

with st.sidebar:
    st.title("Settings")
    st.session_state["intelligence_rating"] = st.selectbox(
        "Intelligence Rating",
        options=["Ultra", "High", "Medium", "Low"],
        index=["Ultra", "High", "Medium", "Low"].index(st.session_state["intelligence_rating"]),
        help="Production AI Models"
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
            
            # Get the result from the graph
            res = graph.invoke(initial_state)
            output_text = res.get("output", "")
            
            # --- Real-Time Streaming Effect ---
            def stream_data():
                import time
                for word in output_text.split(" "):
                    yield word + " "
                    time.sleep(0.04) # Smooth typing effect

            # Display with streaming effect
            st.write_stream(stream_data())
            
            # Save to history
            st.session_state["chat_history"].append({"role": "assistant", "content": output_text})
