from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    The state of the agent.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    task: str # translate, grammar, draft, chat
    intelligence_rating: str # High, Medium, Low
    target_lang: str # English, Amharic, etc.
    output: str
