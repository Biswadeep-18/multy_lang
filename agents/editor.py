from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, EditResponse

def editor_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    input_text = state["messages"][-1].content
    task_type = state.get("task_type", "document")
    
    prompt = f"""You are an elite linguistic editor and communications expert.
Your goal is to refine the provided text to be grammatically flawless while enhancing its tone and clarity.

Instructions:
1. Provide a 'no-bullshit' grammatically perfect version of the text.
2. Enhance the tone based on the context of the writing.
3. You MUST provide your response using the 'EditResponse' tool, which includes the refined text and an explanation of your changes.

Text to refine:
\"\"\"
{input_text}
\"\"\"
"""
    structured_llm = llm.with_structured_output(EditResponse)
    response = structured_llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "messages": [HumanMessage(content=response.refined_text)], 
        "output": response.refined_text,
        "metadata": {
            "explanation": response.explanation
        }
    }
