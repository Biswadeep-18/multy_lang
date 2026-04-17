from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, TranslationResponse

def translation_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    target = state.get("target_lang", "English")
    input_text = state["messages"][-1].content
    
    prompt = f"""You are a highly skilled professional translator. 
Your task is to translate the provided text into {target} while strictly preserving the original tone, context, and nuances.

Follow these rules:
1. Translate to {target}. If {target} is 'English', translate from the source language to English.
2. Maintain the formatting and emotional weight of the original text.
3. You MUST provide your response using the 'TranslationResponse' tool.

Text to translate:
\"\"\"
{input_text}
\"\"\"
"""
    # Use Structured Output
    structured_llm = llm.with_structured_output(TranslationResponse)
    response = structured_llm.invoke([HumanMessage(content=prompt)])
    
    # Store the structured translated text
    return {
        "messages": [HumanMessage(content=response.translated_text)], 
        "output": response.translated_text
    }
