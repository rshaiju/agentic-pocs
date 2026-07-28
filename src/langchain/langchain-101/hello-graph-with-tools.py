from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from typing import Annotated
from typing_extensions import TypedDict
import random
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from src.utilities.send_push_notification import send_notification


MODEL="gpt-5-mini"

class State(TypedDict):
    messages: Annotated[list,add_messages]

@tool
def translate_to_spanish(message:str)->str:
    """This tool can be used to translate any text to Spanish"""
    response=llm_with_tools.invoke(f"Pls translate this into Spanish:{message}.Reply with the translation alone")
    return response.content 

llm_with_tools=ChatOpenAI(model=MODEL).bind_tools([translate_to_spanish])

def silly_node(state: State)->dict:
    nouns=["tomato", "cup", "mobile phone", "mouse pad","key board"]
    adjectives=["wise","foolish", "slow","brilliant","sharp","boring"]
    sentence= f"{random.choice(nouns)} is {random.choice(adjectives)}"
    print(f'silly said: {sentence}')
    return{"messages":[{"role":"user", "content":sentence }]}

def chat_node(state: State)->dict:
    llm_reponse=llm_with_tools.invoke(state["messages"])
    if not llm_reponse.tool_calls:
        print(f'llm responded: { llm_reponse.content}')
    return {"messages": [llm_reponse]}

tools=[translate_to_spanish]

builder=StateGraph(State)
builder.add_node("silly",silly_node)
builder.add_node("chat", chat_node)
builder.add_node("tools",ToolNode(tools))
builder.add_edge(START,"silly")
builder.add_edge("silly","chat")
builder.add_conditional_edges("chat",tools_condition)
builder.add_edge("tools","chat")
builder.add_edge("chat",END)
graph=builder.compile()

result=graph.invoke({"messages":[{"role":"system","content":"you are a witty assistant whoc respond in just a short sentence. replies need not make any sense but must be witty. Also give the message translated in Spanish"}]})




