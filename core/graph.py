from langgraph.graph import StateGraph, END
from core.state import AgentState
from agents.translator import translation_node
from agents.editor import editor_node
from agents.drafter import drafter_node
from agents.chatbot import chatbot_node

def create_graph():
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("translate", translation_node)
    workflow.add_node("grammar", editor_node)
    workflow.add_node("draft", drafter_node)
    workflow.add_node("chat", chatbot_node)
    
    # Define Routing Logic
    def route_task(state: AgentState):
        task = state.get("task", "chat")
        if task == "translate":
            return "translate"
        elif task == "grammar":
            return "grammar"
        elif task == "draft":
            return "draft"
        else:
            return "chat"
    
    # Set Entry Point
    workflow.set_conditional_entry_point(
        route_task,
        {
            "translate": "translate",
            "grammar": "grammar",
            "draft": "draft",
            "chat": "chat"
        }
    )
    
    # All nodes lead to END
    workflow.add_edge("translate", END)
    workflow.add_edge("grammar", END)
    workflow.add_edge("draft", END)
    workflow.add_edge("chat", END)
    
    return workflow.compile()

graph = create_graph()
