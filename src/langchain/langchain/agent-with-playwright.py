from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

load_dotenv(override=True)

client=MultiServerMCPClient({
    "playwright": {
        "transport": "stdio",
         "command" : "npx",
         "args" : ["-y", "@playwright/mcp@latest", "--isolated"]
    }
})



tools=asyncio.run(client.get_tools())

agent=create_agent(
    model="gpt-5-mini",
    tools=tools, 
    system_prompt="You are a web research assistant. Use the browser tools to complete the task, then report clearly."
)

response=asyncio.run(agent.ainvoke({"messages": [HumanMessage(content="Go to https://news.ycombinator.com and tell me the titles of the top three stories on the front page.")]}))

print(response["messages"][-1].content)