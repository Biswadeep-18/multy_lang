from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, EditResponse

def editor_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    input_text = state["messages"][-1].content
    
    prompt = f"""You are an elite linguistic editor. 
Provide a 'no-bullshit' grammatically perfect version of the text and a separate explanation of your improvements.

Text:
{input_text}
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
