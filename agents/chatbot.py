import os
from datetime import datetime
from ddgs import DDGS
from core.llms import get_llm
from core.state import AgentState
from langchain_core.messages import SystemMessage

def chatbot_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    last_msg = state["messages"][-1].content
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # 1. Perform Broad Search for accuracy
    search_keywords = ["search", "find", "who is", "latest", "news", "weather", "today", "current", "cm", "minister"]
    search_results = "No search performed."
    
    if any(keyword in last_msg.lower() for keyword in search_keywords):
        try:
            with DDGS() as ddgs:
                # Increased results and using 'time' parameter if possible (not in standard ddgs text, but we can refine query)
                query = f"{last_msg} {current_date}"
                results = [r for r in ddgs.text(query, max_results=5)]
                if results:
                    search_results = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
                else:
                    search_results = "No results found for your query. Please note that real-time data might be limited."
        except Exception as e:
            search_results = f"Search failed: {str(e)}"

    # 2. Enhanced System Prompt
    system_prompt = (
        f"You are a helpful AI assistant with real-time search capabilities. Today's date is {current_date}.\n"
        "IMPORTANT: Prioritize information found in the search results over your training data, as training data may be outdated (pre-2024).\n"
        "If search results are available, use them to provide the most current answer.\n\n"
        f"--- CURRENT SEARCH RESULTS ---\n{search_results}\n------------------------------\n\n"
        "Be extremely accurate about current political figures and events. If you are unsure, state that the search results were inconclusive."
    )

    # 3. Invoke LLM
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "output": response.content}
