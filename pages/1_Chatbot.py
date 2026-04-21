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
                # Filter out suggestions for the streaming text
                text_lines = [l for l in output_text.split("\n") if not l.startswith(">>")]
                clean_text = "\n".join(text_lines)
                for word in clean_text.split(" "):
                    yield word + " "
                    time.sleep(0.02)

            # Display with streaming effect
            st.write_stream(stream_data())
            
            # --- Parse and Show Suggestions ---
            suggestions = [l.replace(">>", "").strip() for l in output_text.split("\n") if l.startswith(">>")]
            if suggestions:
                st.markdown("---")
                st.markdown("#### Suggested Next Steps")
                cols = st.columns(len(suggestions))
                for idx, suggestion in enumerate(suggestions):
                    if cols[idx].button(suggestion, key=f"sug_{idx}_{len(st.session_state.chat_history)}", use_container_width=True):
                         # If clicked, we set a temporary state to trigger the next loop
                         st.session_state["clicked_suggestion"] = suggestion
                         st.rerun()
            
            # Save to history (Keep suggestions for history if desired, or strip them)
            st.session_state["chat_history"].append({"role": "assistant", "content": output_text})

# Handle Clicked Suggestion (Outside the main input block to avoid context issues)
if "clicked_suggestion" in st.session_state:
    suggestion = st.session_state.pop("clicked_suggestion")
    # Simulate chat input process for the suggestion
    st.session_state["chat_history"].append({"role": "user", "content": suggestion})
    st.rerun()
