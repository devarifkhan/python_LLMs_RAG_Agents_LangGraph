from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    print("Inside Chatbot Node", state)
    return {"messages": [llm.invoke(state["messages"])]}


def samplenode(state: State):
    print("Inside Sample Node", state)
    return {"messages": "Hi, This is a message from LangGraph Sample Node!"}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

DB_URI = "mongodb://admin:admin@localhost:27017"
checkpointer = MongoDBSaver.from_conn_string(DB_URI)
graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": "arifkhan"
    }
}

for chunk in graph_with_checkpointer.stream(
    {"messages": [{"role": "user", "content": "Hello, How are you?"}]},
    config=config,
):
    print("Chunk:", chunk)

print("Done streaming")
