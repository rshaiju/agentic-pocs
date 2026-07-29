import random
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage

MODEL="gpt-5-mini"

load_dotenv(override=True)

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

agent=create_agent(
    model=MODEL,
    system_prompt="You are helpful agent. Use tools to answer your questions. Reply with the answer alone",
    tools=[get_age,get_name]
    )

result=agent.invoke({"messages": [HumanMessage("Who am I and what is my age?")]})
print(result["messages"][-1].content)