from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph_message import add_messages

class StateUpdate(TypedDict):
    messages: Annotated[list,add_messages]