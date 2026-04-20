from typing import TypedDict, Annotated, List, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

# --- Structured Output Models ---
class TranslationResponse(BaseModel):
    translated_text: str = Field(description="The final translated text.")
    detected_language: str = Field(description="The language detected in the source text.")

class EditResponse(BaseModel):
    refined_text: str = Field(description="The full, grammar-corrected and tone-enhanced text.")
    explanation: str = Field(description="A brief explanation of the key grammatical errors fixed or tone improvements made.")

class DraftResponse(BaseModel):
    draft: str = Field(description="The generated high-quality draft.")
    detected_intent: str = Field(description="Context summary.")

# --- State Definition ---
class AgentState(TypedDict):
    """
    The state of the agent.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    task: str # translate, grammar, draft, chat
    intelligence_rating: str # High, Medium, Low
    source_lang: Optional[str] # English, French, detect, etc.
    target_lang: Optional[str] # English, Amharic, etc.
    task_subtype: Optional[str]
    output: str
    metadata: Optional[dict] = None
