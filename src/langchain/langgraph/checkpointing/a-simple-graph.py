from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI

MODEL="gpt-5-mini"

class State(TypedDict):
    messages: Annotated[list,add_messages]

def ask_llm(state: State)->dict:
    llm=ChatOpenAI(model=MODEL)
    response=llm.invoke(state["messages"])
    print(response.content)


builder=StateGraph(State)
builder.add_node("ask_llm",ask_llm)

builder.add_edge(START,"ask_llm")
builder.add_edge("ask_llm",END)

graph=builder.compile()

graph.invoke({"messages":[{"role":"system","content":"You are a helpful assistant who tells jokes. Reply with the joke alone"},{"role":"user","content":"Tell me a joke"}]})

