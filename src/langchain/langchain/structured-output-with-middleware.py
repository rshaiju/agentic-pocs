import random

from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.messages import HumanMessage
from langchain.agents.middleware import wrap_tool_call
from pydantic import BaseModel, Field

MODEL="gpt-5-mini"

load_dotenv(override=True)

class City_Report(BaseModel):
    city:str=Field(description="The city name")
    population:str=Field(description="Population of the city")
    weather:str=Field(description="Weather of the city")

@tool
def get_weather(city:str)->str:
    """Tool to get the weather of the given city"""
    return f"{random.randint(1,40)} degrees"

@tool
def get_population(city:str)->str:
    """Tool to get the population of the given city"""
    return f"{random.randint(1,150)} Million"

@wrap_tool_call
def log_tool_calls(request,handler):
    call=request.tool_call
    print(f"[middleware] calling {call["name"]} with args{call["args"]} ")
    return handler(request)

agent=create_agent(
    model=MODEL,
    system_prompt="You an assistant who uses your tools to produce a report of the given city",
    tools=[get_population,get_weather],
    response_format=City_Report,
    middleware=[log_tool_calls]
    )

report=agent.invoke({"messages":[HumanMessage("Mumbai")]})["structured_response"]
print("name:" + report.city)
print("population:" + report.population)
print("weather:" + report.weather)

