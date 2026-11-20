"""
LangGraph chat with a MongoDB checkpointer.

Every step of the graph is saved in MongoDB under a thread_id, so the
conversation survives restarts: run the script twice and the message count grows.

Start MongoDB first:  docker compose up -d   (credentials come from .env)
"""

import os
import sys
from typing import Annotated
from urllib.parse import quote_plus

from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_openai import ChatOpenAI

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")

if not MONGO_USERNAME or not MONGO_PASSWORD:
    sys.exit("Set MONGO_USERNAME and MONGO_PASSWORD in .env (see .env.example).")

DB_URI = (
    f"mongodb://{quote_plus(MONGO_USERNAME)}:{quote_plus(MONGO_PASSWORD)}"
    f"@{MONGO_HOST}:{MONGO_PORT}"
)

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))


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


def main():
    config = {"configurable": {"thread_id": "demo-thread"}}

    # from_conn_string is a context manager: it opens and closes the Mongo client.
    with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)

        for chunk in graph_with_checkpointer.stream(
            {"messages": [{"role": "user", "content": "Hello, How are you?"}]},
            config=config,
        ):
            print("Chunk:", chunk)

        print("Done streaming")

        # Read the saved state back from MongoDB to show that it was persisted.
        saved = graph_with_checkpointer.get_state(config)
        print(f"Messages stored in MongoDB for this thread: {len(saved.values['messages'])}")


if __name__ == "__main__":
    main()
