from typing import Optional
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langraph.graph import StateGraph,START,END


load_dotenv()


class State(TypedDict):
    user_input: str
    llm_output: Optional[str]
    is_good: Optional[bool]
    
def chatbot(state:State):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state["user_input"]},
        ],
    )
    state["llm_output"] = response.choices[0].message.content
    return state
    
def evaluate_response(state:State)-> Literal["chatbot_gemini","endnode"]:
    if True:
        return 'endnode'
    
    return "The response was not satisfactory."


def endcode(state:State):
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode", endcode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edge("chatbot","evaluate_response")
graph_builder.add_edge("chatbot_gemini", "encode")
graph_builder.add_edge("endnode", END)


graph = graph_builder.compile() 

updated_state= graph.invoke(State({"user_query":"Hello, how are you?"}))
print(updated_state)