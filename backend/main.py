from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from langchain_core.messages import HumanMessage
from core.graph import graph
from core.config import get_flattened_languages

# --- Swagger Metadata ---
tags_metadata = [
    {
        "name": "System",
        "description": "Health checks and configuration endpoints.",
    },
    {
        "name": "AI Processing",
        "description": "Core AI endpoints for translation, grammar correction, and content drafting.",
    },
]

app = FastAPI(
    title="Translate.AI - Advanced Multi-Language Engine",
    description="""
    ## Enterprise Translation & Linguistic Intelligence
    
    Translate.AI provides high-fidelity translation, grammar refinement, and professional drafting capabilities.
    
    ### Key Features:
    * **Detect & Translate**: Support for 100+ languages including regional scripts like Odia.
    * **Grammar Intelligence**: Native-level tone and structure refinement.
    * **Professional Drafting**: Context-aware content generation.
    """,
    version="1.2.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "EazzDocs Support",
        "url": "https://eazzdocs.ai/support",
    }
)

# --- Models ---

class AssistantRequest(BaseModel):
    text: str = Field(..., json_schema_extra={"example": "Translate this text into Odia."}, description="The input text to be processed.")
    task: str = Field(..., json_schema_extra={"example": "translate"}, description="The type of task: translate, grammar, draft, or chat.")
    intelligence_rating: str = Field("Medium", json_schema_extra={"example": "High"}, description="Model intelligence level: Low, Medium, High, Ultra.")
    source_lang: Optional[str] = Field(None, json_schema_extra={"example": "English"}, description="Source language (or 'Detect Language').")
    target_lang: Optional[str] = Field(None, json_schema_extra={"example": "Odia"}, description="Target language for translation/drafting.")
    task_subtype: Optional[str] = Field(None, json_schema_extra={"example": "email"}, description="Sub-type for drafting: email, document, research, custom.")

class AssistantResponse(BaseModel):
    output: str = Field(..., description="The AI generated result.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional processing metadata (e.g. detected language).")
    task: str = Field(..., description="The task that was performed.")

# --- Internal Helper ---

def invoke_graph(request: AssistantRequest):
    initial_state = {
        "messages": [HumanMessage(content=request.text)],
        "task": request.task,
        "intelligence_rating": request.intelligence_rating,
        "source_lang": request.source_lang,
        "target_lang": request.target_lang,
        "task_subtype": request.task_subtype
    }
    
    try:
        result = graph.invoke(initial_state)
        return {
            "output": result["output"],
            "metadata": result.get("metadata", {}),
            "task": request.task
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoints ---

@app.get("/", tags=["System"])
def read_root():
    """Health check endpoint to verify system status."""
    return {"status": "online", "message": "Translate.AI API is running and healthy"}

@app.get("/languages", tags=["System"])
def get_languages():
    """Returns a list of all supported languages for translation and drafting."""
    return {"languages": get_flattened_languages()}

@app.post("/process", response_model=AssistantResponse, tags=["AI Processing"])
def process_task(request: AssistantRequest):
    """
    **Unified Processing Endpoint**
    
    This endpoint can handle any supported task (translation, grammar, drafting, or chat)
    based on the 'task' parameter in the request body.
    """
    return invoke_graph(request)

@app.post("/process/translate", response_model=AssistantResponse, tags=["AI Processing"])
def translate_text(
    text: str = Body(..., examples=["Hello, how are you?"]),
    target_lang: str = Body(..., examples=["Odia"]),
    source_lang: str = Body("Detect Language"),
    intelligence: str = Body("Medium")
):
    """Specific step for translation."""
    req = AssistantRequest(
        text=text, 
        task="translate", 
        target_lang=target_lang, 
        source_lang=source_lang,
        intelligence_rating=intelligence
    )
    return invoke_graph(req)

@app.post("/process/grammar", response_model=AssistantResponse, tags=["AI Processing"])
def refine_grammar(
    text: str = Body(..., examples=["Me is going to store."]),
    target_lang: str = Body("English"),
    intelligence: str = Body("Medium")
):
    """Specific step for grammar and tone refinement."""
    req = AssistantRequest(
        text=text, 
        task="grammar", 
        target_lang=target_lang,
        intelligence_rating=intelligence
    )
    return invoke_graph(req)

@app.post("/process/draft", response_model=AssistantResponse, tags=["AI Processing"])
def generate_draft(
    prompt: str = Body(..., examples=["Write a formal leave application for 2 days."]),
    target_lang: str = Body("English"),
    subtype: str = Body("email"),
    intelligence: str = Body("Medium")
):
    """Specific step for professional content drafting."""
    req = AssistantRequest(
        text=prompt, 
        task="draft", 
        target_lang=target_lang,
        task_subtype=subtype,
        intelligence_rating=intelligence
    )
    return invoke_graph(req)

@app.post("/process/chat", response_model=AssistantResponse, tags=["AI Processing"])
def general_chat(
    message: str = Body(..., examples=["What are the benefits of learning Odia?"]),
    intelligence: str = Body("Medium")
):
    """General AI chatbot interaction step."""
    req = AssistantRequest(
        text=message, 
        task="chat", 
        intelligence_rating=intelligence
    )
    return invoke_graph(req)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
