from turtle import up
from typing_extensions import TypedDict
from typing import Annotated
from asyncio import graph
from langgraph.graph_message import add_messages
from langgraph.graph import StateGraph,START,END

class State(TypedDict):
    messages: Annotated[list,add_messages]
    

def chatbot(state: State):
    print("Inside Chatbot Node",state)
    return {"messages": "Hi, This is a message from LangGraph Chatbot Node!"}

def samplenode(state: State):
    print("Inside Sample Node",state)
    return {"messages": "Hi, This is a message from LangGraph Sample Node!"}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

graph = graph_builder.compile()

updated_state=graph.invoke(State(
    messages=["Hi, This is the initial message to start the workflow."]
))

print("Updated State Graph:",updated_state)