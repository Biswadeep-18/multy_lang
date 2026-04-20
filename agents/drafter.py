from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, DraftResponse

def drafter_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])
    input_text = state["messages"][-1].content
    task_type = state.get("task_subtype", "document")
    target = state.get("target_lang", "English")

    prompt = f"""You are a professional world-class writer specializing in {task_type}s.
Your mission is to draft a high-quality {task_type} written entirely in {target}.

### GUIDELINES:
1. **Language**: The ENTIRE output must be written in {target}. Use the correct native script.
2. **Depth & Quality**: The content must be well-structured and professional.
3. **Structure**:
   - **Email**: Must include a subject line followed by the body.
   - **Document**: Must use clear headings and logical flow.
   - **Research**: Must maintain an objective and technical style.
4. **CRITICAL**: Return ONLY the {task_type}. Do NOT include any introductory sentences, meta-talk, or phrases like "Here is your document".
5. **Tool Usage**: You MUST provide your response using the 'DraftResponse' tool.

### INPUT INSTRUCTIONS/NOTES:
\"\"\"
{input_text}
\"\"\"

Final Check:
- Task type: {task_type}
- Output Language: {target}
"""
    # Use Structured Output with a safer method for Groq
    structured_llm = llm
    if hasattr(llm, "with_structured_output"):
        method = "json_mode" if "ChatGroq" in str(type(llm)) else None
        structured_llm = llm.with_structured_output(DraftResponse, method=method)

    try:
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        
        if hasattr(response, 'draft'):
            draft = response.draft
        else:
            # Fallback for plain string response
            draft = str(response.content) if hasattr(response, 'content') else str(response)
    except Exception:
        # Final fallback: raw LLM call
        raw_response = llm.invoke([HumanMessage(content=prompt)])
        draft = raw_response.content

    # Final Clean: Remove AI artifact headers if they leaked into the text
    final_output = draft.strip()
    bad_headers = ["DraftResponse", "Subject:", "Draft:", "Generated Document:", "Title:"]
    # We maintain "Subject:" for emails as requested in structure, 
    # but we remove the AI wrapper text if it leaked "DraftResponse"
    for header in ["DraftResponse", "Generated Document:"]:
        if final_output.startswith(header):
            parts = final_output.split("\n", 1)
            if len(parts) > 1:
                final_output = parts[1].strip()

    return {
        "messages": [HumanMessage(content=final_output)],
        "output": final_output
    }
