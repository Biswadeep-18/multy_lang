from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from langchain_core.messages import HumanMessage
from core.graph import graph
from core.config import get_flattened_languages

app = FastAPI(
    title="Translate.AI Backend",
    description="Enterprise-grade Translation and Drafting API",
    version="1.0.0"
)

# --- Models ---

class AssistantRequest(BaseModel):
    text: str
    task: str # translate, grammar, draft
    intelligence_rating: str = "Medium"
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None
    task_subtype: Optional[str] = None

class AssistantResponse(BaseModel):
    output: str
    metadata: Optional[dict] = None
    task: str

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"status": "online", "message": "Translate.AI API is running"}

@app.get("/languages")
def get_languages():
    """Returns a list of all supported languages."""
    return {"languages": get_flattened_languages()}

@app.post("/process", response_model=AssistantResponse)
def process_task(request: AssistantRequest):
    """
    Unified endpoint to process translation, grammar, or drafting tasks.
    """
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
