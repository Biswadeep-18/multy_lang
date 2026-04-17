from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, DraftResponse

def drafter_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    input_text = state["messages"][-1].content
    task_type = state.get("task_subtype", "document")
    
    prompt = f"""You are a professional world-class writer specializing in {task_type}s.
Your goal is to draft high-quality content based precisely on the instructions or notes provided.

Instructions:
1. Ensure the content is research-backed, objective, or creative as per the {task_type} context.
2. Email requirement: Provide a professional and clear subject line.
3. Document requirement: Structured with clear headings and logical flow.
4. Research requirement: Objective, well-sourced, and technical style.
5. You MUST provide your response using the 'DraftResponse' tool.

Input Notes/Instructions:
\"\"\"
{input_text}
\"\"\"
"""
    structured_llm = llm.with_structured_output(DraftResponse)
    response = structured_llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "messages": [HumanMessage(content=response.draft)], 
        "output": response.draft
    }
