from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

MODEL="gpt-5-mini"

load_dotenv(override=True)

llm=ChatOpenAI(model=MODEL)

@tool
def say_hola():
    """This tool can be used to say hola"""
    return "Hola mate!!"

llm_with_tools=llm.bind_tools([say_hola])

conversation=[
    SystemMessage("You are a helpful assistant who will use a given tool to say hola"),
    HumanMessage("Say Hola")
    ]

response=llm_with_tools.invoke(conversation);
conversation.append(response)

for tool_call in response.tool_calls:
    if tool_call["name"]=="say_hola":
        result= say_hola.invoke(tool_call["args"])
        conversation.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"] ))

final=llm_with_tools.invoke(conversation)

print(final.content)
