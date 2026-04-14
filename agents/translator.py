from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, TranslationResponse

def translation_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    target = state.get("target_lang", "English")
    input_text = state["messages"][-1].content
    
    prompt = f"""You are a professional translator. 
Translate the following text to {target}.
If the target is 'English', translate from any language to English.
Preserve the tone and context.

Text to translate:
{input_text}
"""
    # Use Structured Output
    structured_llm = llm.with_structured_output(TranslationResponse)
    response = structured_llm.invoke([HumanMessage(content=prompt)])
    
    # Store the structured translated text
    return {
        "messages": [HumanMessage(content=response.translated_text)], 
        "output": response.translated_text
    }
