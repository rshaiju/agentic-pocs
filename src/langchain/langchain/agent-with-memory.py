from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.messages import HumanMessage
from langchain.tools import tool
import gradio as gr
import os
import random

MODEL="gpt-5-mini"

@tool
def get_name()->str:
    """Returns my name"""
    print("Executing get_name")
    return "My name is John Doe"

@tool
def get_age()->int:
    """Returns my age"""
    print("Executing get_age")
    return random.randint(a=1,b=120)

load_dotenv(override=True)


def chat(message:str,history):
    with SqliteSaver.from_conn_string("memory.db") as sql_memory:
        agent=create_agent(model=MODEL,system_prompt="You are a helpful assistant. You will use tools to answer. Respond with the answer alone", checkpointer=sql_memory, tools=[get_name,get_age])
        config={"configurable":{"thread_id":os.path.basename(__file__)}}
        response=agent.invoke({"messages":[HumanMessage(message)]},config=config)
    return response["messages"][-1].content

gr.ChatInterface(fn=chat).launch(inbrowser=True)


