from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
import random

MODEL="gpt-5-mini"

class State(TypedDict):
    messages: Annotated[list,add_messages]

def silly_node(state: State)->dict:
    nouns=["tomato", "cup", "mobile phone", "mouse pad","key board"]
    adjectives=["wise","foolish", "slow","brilliant","sharp","boring"]
    sentence= f"{random.choice(nouns)} is {random.choice(adjectives)}"
    print(f'silly said: {sentence}')
    return{"messages":[{"role":"user", "content":sentence }]}

def chat_node(state: State)->dict:
    llm=ChatOpenAI(model=MODEL)
    llm_reponse=llm.invoke(state["messages"])
    print(f'llm responded: { llm_reponse.content}')
    return {"meesages": [llm.invoke(state["messages"])]}


builder=StateGraph(State)
builder.add_node("silly",silly_node)
builder.add_node("chat", chat_node)
builder.add_edge(START,"silly")
builder.add_edge("silly","chat")
builder.add_edge("chat",END)
graph=builder.compile()

result=graph.invoke({"messages":[{"role":"system","content":"you are a witty assistant whoc respond in just a short sentence. replies need not make any sense but must be witty"},
                                 {"role":"user","content":"say something!!"}]})




