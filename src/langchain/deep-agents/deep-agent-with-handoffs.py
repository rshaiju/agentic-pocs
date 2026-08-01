from deepagents import create_deep_agent
import os
from dotenv import load_dotenv
from deepagents.backends import FilesystemBackend
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv(override=True)

sandbox=os.path.abspath("sandbox")
os.makedirs(sandbox,exist_ok=True)

search=GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())

research_officer_prompt="""
    You are a research director. 
    You will direct the research process of the chosen topic.
    You will plan your research using a todo tool.
    You will delegate research tasks to subagents.
    Findings of the subagents will be delegated to a reporting agent.
    You will validate and apprrove the final report.
"""

research_agent_prompt="""
    You are a research agent.
    You will do research on the assigned topic.
    You will write your findings as a tiny markdown briefing to a file.
    You will be using tools to do your research and write your findings.
"""

reporting_agent_prompt="""
    You are a reporting agent.
    You will write a report based on the findings of the research agents.
    You will prepare a powerpoint presentation based on the report.
    You will be using tools to write the report and prepare the presentation.
"""


research_agent={
    "name": "research_agent",
    "system_prompt": research_agent_prompt,
    "description": "This agent is responsible for conducting research on the assigned topic and writing findings as a tiny markdown briefing to a file."
}

reporting_agent={
    "name": "reporting_agent",
    "system_prompt": reporting_agent_prompt,
    "description": "This agent is responsible for writing reports based on research findings and preparing presentations."
}

research_officer_agent=create_deep_agent(
    model=ChatOpenAI(model="gpt-5"),
    tools=[search],
    system_prompt=research_officer_prompt,
    subagents=[research_agent, reporting_agent],
    backend=FilesystemBackend(root_dir=sandbox, virtual_mode=True)
)

brief="""
Research on top 5 innovative ideas for using agentic solutions for DevOps consultants
The solutions should be innovative and should have tangible benefits for DevOps consultants.
Both the customer and the DevOps consultants should benefit from the solutions.
"""

research_officer_agent.invoke({"messages":[HumanMessage(content=brief)]})
