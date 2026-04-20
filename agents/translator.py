from langchain_core.messages import HumanMessage
from core.llms import get_llm
from core.state import AgentState, TranslationResponse

# Map of language display names to language names understood by LLMs
LANGUAGE_ALIASES = {
    "Odia (Oriya)": "Odia (also known as Oriya), written in Odia script (ଓଡ଼ିଆ)",
    "English (Associate)": "English",
    "Manipuri (Meitei)": "Meitei (Manipuri)",
}

def translation_node(state: AgentState):
    llm = get_llm(state["intelligence_rating"])

    # Resolve target and source language aliases
    raw_target = state.get("target_lang", "English") or "English"
    raw_source = state.get("source_lang", "auto-detect") or "auto-detect"

    target = LANGUAGE_ALIASES.get(raw_target, raw_target)
    # source: if it's "Detect Language" or similar, replace with "auto-detect"
    if raw_source in ("Detect Language", "detect", "", None):
        source = "auto-detect"
    else:
        source = LANGUAGE_ALIASES.get(raw_source, raw_source)

    input_text = state["messages"][-1].content

    prompt = f"""Translate exactly and ONLY the text below into {target}.
Do NOT include any preamble, headers, or metadata.
Return ONLY the translation.

Text:
\"\"\"
{input_text}
\"\"\""""

    # Use Structured Output with a safer method for Groq
    structured_llm = llm
    if hasattr(llm, "with_structured_output"):
        method = "json_mode" if "ChatGroq" in str(type(llm)) else None
        structured_llm = llm.with_structured_output(TranslationResponse, method=method)

    try:
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        
        if isinstance(response, dict):
            translated = response.get("translated_text", "")
            detected = response.get("detected_language", raw_source)
        elif hasattr(response, "translated_text"):
            translated = response.translated_text
            detected = getattr(response, "detected_language", raw_source)
        else:
            # Most aggressive fallback for non-compliant model responses
            content = getattr(response, "content", str(response))
            translated = str(content)
            detected = raw_source
    except Exception:
        raw_response = llm.invoke([HumanMessage(content=prompt)])
        translated = raw_response.content
        detected = raw_source

    # Final Aggressive Clean: Remove any AI metadata artifacts
    final_output = translated.strip()
    # List of metadata strings models sometimes leak when told to use JSON mode
    leak_keywords = ["{", "}", "translated_text", "detected_language", "TranslationResponse", ": \"", "Source Language", "Target Language", "Here is the translation"]
    
    # If the output starts with a JSON-like bracket or a known header, try to extract the meat
    for kw in leak_keywords:
        if final_output.startswith(kw) or (kw in final_output[:50] and "\n" in final_output):
             # If it looks like a JSON block but leaked into string
             if '"translated_text":' in final_output:
                 import re
                 match = re.search(r'"translated_text":\s*"([^"]+)"', final_output)
                 if match:
                     final_output = match.group(1)

    # Secondary line cleaning for headers
    bad_headers = [
        "TranslationResponse", "Source Language:", "Target Language:", "Script:", 
        "Here is the translation:", "Translation:", "Translated Text:", "Language Identification:",
        "Original Language:", "Detected Language:", "Output:", "Text:", "Target Text:"
    ]
    for header in bad_headers:
        if final_output.startswith(header):
            parts = final_output.split("\n", 1)
            if len(parts) > 1:
                final_output = parts[1].strip()
        # Also check if it's in the first line but not the start
        elif header in final_output.split("\n")[0]:
             parts = final_output.split("\n", 1)
             if len(parts) > 1:
                 final_output = parts[1].strip()

    return {
        "messages": [HumanMessage(content=final_output)],
        "output": final_output,
        "metadata": {"detected_language": detected},
    }
