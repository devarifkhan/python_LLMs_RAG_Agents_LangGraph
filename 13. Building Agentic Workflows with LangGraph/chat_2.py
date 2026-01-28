from typing import Optional, Literal
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI


load_dotenv()

client = OpenAI()


class State(TypedDict):
    user_input: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state: State):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state["user_input"]},
        ],
    )
    state["llm_output"] = response.choices[0].message.content
    return state


def chatbot_gemini(state: State):
    # Placeholder for Gemini chatbot - implement as needed
    return state


def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    # Replace with actual evaluation logic
    if state.get("is_good", True):
        return "endnode"
    return "chatbot_gemini"


def endnode(state: State):
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)


graph = graph_builder.compile()

updated_state = graph.invoke({"user_input": "Hello, how are you?"})
print(updated_state)
