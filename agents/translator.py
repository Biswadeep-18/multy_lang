from langchain_core.messages import SystemMessage, HumanMessage
from core.llms import get_llm
from core.state import AgentState

def translation_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    target = state.get("target_lang", "English")
    
    # Get the last message content
    input_text = state["messages"][-1].content
    
    prompt = f"""You are a professional translator. 
Translate the following text to {target}.
If the target is 'English', translate from any language to English.
If the target is Ethiopian/African/Arabic, choose the most appropriate dialect unless specified.
Preserve the tone and context.

Text to translate:
{input_text}
"""
    
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"messages": [response], "output": response.content}
