from langchain_core.messages import SystemMessage
from core.llms import get_llm
from core.state import AgentState

def editor_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    input_text = state["messages"][-1].content
    
    prompt = """You are an expert editor. 
Fix the grammar, spelling, and enhance the tone of the provided text.
Ensure it sounds professional yet engaging. Do not change the core meaning.

Text:
{text}
"""
    
    response = llm.invoke([SystemMessage(content=prompt.format(text=input_text))])
    return {"messages": [response], "output": response.content}
