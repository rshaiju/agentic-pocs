from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
import gradio as gr
from langgraph.checkpoint.sqlite import SqliteSaver

MODEL="gpt-5-mini"

class State(TypedDict):
    messages: Annotated[list,add_messages]

def llm_invoke(state:State)->dict:
    llm =ChatOpenAI(model=MODEL)
    response=llm.invoke(state["messages"])
    print(f"llm responded:{response.content}")
    return {"messages":[response]}

builder=StateGraph(State)
builder.add_node("llm_invoke",llm_invoke)

builder.add_edge(START,"llm_invoke")
builder.add_edge("llm_invoke",END)

def chat(message:str,history):
    config={"configurable":{"thread_id":"my-chat-session"}}
    with SqliteSaver.from_conn_string("memory.db") as sql_memory:
        graph=builder.compile(checkpointer=sql_memory)
        result=graph.invoke({"messages":[{"role":"user","content":message}]},config=config)
    return result["messages"][-1].content

gr.ChatInterface(fn=chat).launch(inbrowser=True)





