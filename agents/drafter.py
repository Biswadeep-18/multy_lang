from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, DraftResponse

def drafter_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    input_text = state["messages"][-1].content
    task_type = state.get("task_subtype", "document")
    
    target = state.get("target_lang", "English")
    
    prompt = f"""You are a professional world-class writer specializing in {task_type}s.
Draft a high-quality {task_type} in {target} based on the following instructions or notes:

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

Requirements:
- Language: {target}
- If email: Professional and clear subject line.
- If document: Structured with headings.
- If research: Objective and well-sourced style.
"""
    structured_llm = llm.with_structured_output(DraftResponse)
    response = structured_llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "messages": [HumanMessage(content=response.draft)], 
        "output": response.draft
    }
