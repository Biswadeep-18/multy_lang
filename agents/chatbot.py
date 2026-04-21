import os
from datetime import datetime
from duckduckgo_search import DDGS
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
                # Optimized query: Raw message + simple 'latest news' keyword
                query = f"{last_msg} latest news"
                search_iter = ddgs.text(query, max_results=5)
                results = [r for r in search_iter]
                
                if results:
                    search_results = "\n".join([f"- {r.get('title', 'No Title')}: {r.get('body', 'No Content')}" for r in results])
                else:
                    # Fallback retry without 'latest news'
                    search_iter = ddgs.text(last_msg, max_results=3)
                    results = [r for r in search_iter]
                    if results:
                        search_results = "\n".join([f"- {r.get('title', 'No Title')}: {r.get('body', 'No Content')}" for r in results])
                    else:
                        search_results = "No specific news found. Use internal knowledge for well-known figures."
        except Exception as e:
            search_results = "Search interface busy. Use internal knowledge."

    # 2. Enhanced System Prompt
    system_prompt = (
        f"You are a highly intelligent AI assistant. Today's date is {current_date}.\n"
        "Your goal is to provide precise, accurate, and insightful answers.\n\n"
        "### REAL-TIME KNOWLEDGE\n"
        f"{search_results}\n\n"
        "### INSTRUCTIONS\n"
        "1. Use the search results provided above as your primary source of truth for current events.\n"
        "2. If search results are missing or inconclusive, use your sophisticated internal logic to provide the most likely correct answer, but maintain professional honesty.\n"
        "3. ALWAYS provide a direct answer. Never say 'I am unable' unless it is absolutely impossible.\n"
        "4. At the VERY END of your response, you MUST provide exactly 5 suggested follow-up questions that the user might want to ask next.\n"
        "Format the suggestions exactly like this (one per line, prefixed with '>>'):\n"
        ">> Clickable Suggestion 1\n"
        ">> Clickable Suggestion 2\n"
        ">> Clickable Suggestion 3\n"
        ">> Clickable Suggestion 4\n"
        ">> Clickable Suggestion 5"
    )

    # 3. Invoke LLM
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])
    return {"messages": [response], "output": response.content}
