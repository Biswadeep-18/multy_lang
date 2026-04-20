from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, EditResponse

def editor_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    input_text = state["messages"][-1].content
    target = state.get("target_lang", "English")

    prompt = f"""You are an elite linguistic editor and communications expert for the {target} language.
Your goal is to refine the provided text in {target} to be grammatically flawless while enhancing its tone and clarity.

Instructions:
1. Provide a polished, grammatically perfect version of the text in {target}.
2. Use the correct native script for {target} (e.g., Devanagari for Hindi, Odia script for Odia, etc.).
3. Enhance the tone and flow while preserving the original meaning.
4. **CRITICAL**: Return ONLY the refined text. Do NOT include any intro, explanation inside the text, or conversational filler.
5. You MUST provide your response using the 'EditResponse' tool.

Text to refine ({target}):
\"\"\"
{input_text}
\"\"\"
"""
    # Use Structured Output with a safer method for Groq
    structured_llm = llm
    if hasattr(llm, "with_structured_output"):
        method = "json_mode" if "ChatGroq" in str(type(llm)) else None
        structured_llm = llm.with_structured_output(EditResponse, method=method)

    try:
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        
        if hasattr(response, 'refined_text'):
            refined = response.refined_text
            explanation = response.explanation
        else:
            # Fallback for plain string response
            refined = str(response.content) if hasattr(response, 'content') else str(response)
            explanation = "Polished for grammar and clarity."
    except Exception:
        # Final fallback: raw LLM call
        raw_response = llm.invoke([HumanMessage(content=prompt)])
        refined = raw_response.content
        explanation = "AI refined the text automatically."

    # Final Clean: Remove AI artifact headers if they leaked into the text
    final_output = refined.strip()
    bad_headers = ["EditResponse", "Refined Text:", "Explanation:", "Polished Version:", "Grammar Fix:"]
    for header in bad_headers:
        if final_output.startswith(header):
            parts = final_output.split("\n", 1)
            if len(parts) > 1:
                final_output = parts[1].strip()

    return {
        "messages": [HumanMessage(content=final_output)],
        "output": final_output,
        "metadata": {"explanation": explanation}
    }
