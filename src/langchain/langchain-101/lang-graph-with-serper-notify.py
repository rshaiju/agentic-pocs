import random
from typing import Annotated

from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from src.utilities.send_push_notification import send_notification

MODEL="gpt-5-mini"

class State(TypedDict):
    messages: Annotated[list,add_messages]

search=GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())

@tool
def notify_user(title:str,message:str):
    """Send a push notification to user's phone"""
    send_notification(title,message)

llm_with_tools=ChatOpenAI(model=MODEL).bind_tools([search,notify_user])


def chat_node(state: State)->dict:
    llm_reponse=llm_with_tools.invoke(state["messages"])
    print(f'llm responded: { llm_reponse.content}')
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

tools=[search,notify_user]


builder=StateGraph(State)
builder.add_node("chat", chat_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START,"chat")
builder.add_conditional_edges("chat",tools_condition)
builder.add_edge("tools","chat")
builder.add_edge("chat",END)
graph=builder.compile()

result=graph.invoke({"messages":[{"role":"system","content":"You are a helpful assistant equipped with tools. You will make use of tools to search for details of the given topic. You will summrize the resulsts to a one-liner. Respond with the summary alone, and send the summary as a push notification to user's phone]"},
                                 {"role":"user","content":"Abracadabra!!"}]})




