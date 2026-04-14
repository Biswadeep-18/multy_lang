from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState

def drafter_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    input_text = state["messages"][-1].content
    task_type = state.get("task_subtype", "document") # email, document, research
    
    prompt = f"""You are a professional writer specializing in {task_type}s.
Draft a high-quality {task_type} based on the following instructions or notes:

Input:
{input_text}

Requirement:
- If email: Professional and clear subject line.
- If document: Structured with headings.
- If research: Objective and well-sourced style.
"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [response], "output": response.content}
