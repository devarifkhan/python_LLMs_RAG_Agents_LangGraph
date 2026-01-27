from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph_message import add_messages
from langgraph.graph import StateGraph

class State(TypedDict):
    messages: Annotated[list,add_messages]
    

def chatbot(state: State):
    return {"messages": "Hi, This is a message from LangGraph Chatbot Node!"}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
