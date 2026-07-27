from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
import random

class State(TypedDict):
    messages: Annotated[list,add_messages]


def silly_node(state: State)->dict:
    nouns=["tomato", "cup", "mobile phone", "mouse pad","key board"]
    adjectives=["wise","foolish", "slow","brilliant","sharp","boring"]
    sentence= f"{random.choice(nouns)} is {random.choice(adjectives)}"
    return{"messages":[{"role":"assistant", "content":sentence }]}

builder=StateGraph(State)
builder.add_node("silly",silly_node)
builder.add_edge(START,"silly")
builder.add_edge("silly",END)
graph=builder.compile()

result=graph.invoke({"messages":{"role":"user","content":"say something!!"}})
print(result["messages"][-1].content)


