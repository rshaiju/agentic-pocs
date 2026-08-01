from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv
import os
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper


sandbox=os.path.abspath("sandbox")
os.makedirs(sandbox,exist_ok=True)

load_dotenv(override=True)

search=GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())

open_ai_agent=ChatOpenAI(model="gpt-5-mini")

agent = create_deep_agent(
    model=open_ai_agent,
    tools=[search],
    system_prompt="You are a research analyst. Plan with your todo tool."\
    "Use the search tool to gather information. Write your findings as tiny markdown briefing to a file",
    backend=FilesystemBackend(root_dir=sandbox, virtual_mode=True)
)

brief="""
Our company is planning to move it's sales fleet of 100 cars to EV
Do a research on the top 2 EVS in the market
Do a comparison of the top 2 EVS in terms of range, price, and features.
Write your findings as a tiny markdown briefing to a file.
"""

agent.invoke({"messages":[HumanMessage(content=brief)]})