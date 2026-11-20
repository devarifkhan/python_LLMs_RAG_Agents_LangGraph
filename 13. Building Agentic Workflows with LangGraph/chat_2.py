"""
LangGraph workflow with an LLM-as-judge and a fallback model.

    START -> chatbot (OpenAI) -> evaluate (judge) --good--> endnode -> END
                                                  `--bad---> chatbot_gemini -> endnode

1. `chatbot` answers the user with an OpenAI model.
2. `evaluate` asks an LLM to judge whether the answer is good (strict JSON, validated by Pydantic).
3. If the answer is not good, `chatbot_gemini` answers again with Gemini.

Needs OPENAI_API_KEY and GOOGLE_API_KEY in .env.
"""

import os
import json
from typing import Optional, Literal

from dotenv import load_dotenv
from typing_extensions import TypedDict
from pydantic import BaseModel, ValidationError
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_MODEL = "gemini-2.5-flash"

openai_client = OpenAI()
gemini_client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


class State(TypedDict):
    user_input: str
    llm_output: Optional[str]
    is_good: Optional[bool]
    answered_by: Optional[str]


class Evaluation(BaseModel):
    is_good: bool
    reason: str


def chatbot(state: State):
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state["user_input"]},
        ],
    )
    return {"llm_output": response.choices[0].message.content, "answered_by": OPENAI_MODEL}


def evaluate(state: State):
    """LLM-as-judge: is the answer correct, relevant and complete?"""
    prompt = f"""Judge whether the ANSWER is a correct, relevant and complete reply to the QUESTION.
Return ONLY JSON: {{"is_good": true/false, "reason": "one sentence"}}

QUESTION: {state["user_input"]}
ANSWER: {state["llm_output"]}"""

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    try:
        evaluation = Evaluation(**json.loads(response.choices[0].message.content))
    except (json.JSONDecodeError, ValidationError, TypeError):
        # If the judge's output can't be parsed, be safe and get a second answer.
        evaluation = Evaluation(is_good=False, reason="Judge output could not be parsed")

    print(f"Evaluation: is_good={evaluation.is_good} ({evaluation.reason})")
    return {"is_good": evaluation.is_good}


def route_after_evaluation(state: State) -> Literal["chatbot_gemini", "endnode"]:
    return "endnode" if state.get("is_good") else "chatbot_gemini"


def chatbot_gemini(state: State):
    response = gemini_client.chat.completions.create(
        model=GEMINI_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Give a correct, complete answer."},
            {"role": "user", "content": state["user_input"]},
        ],
    )
    return {"llm_output": response.choices[0].message.content, "answered_by": GEMINI_MODEL}


def endnode(state: State):
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("evaluate", evaluate)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "evaluate")
graph_builder.add_conditional_edges("evaluate", route_after_evaluation)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()


if __name__ == "__main__":
    updated_state = graph.invoke({"user_input": "Hello, how are you?"})
    print(f"\nAnswered by {updated_state['answered_by']}:\n{updated_state['llm_output']}")
