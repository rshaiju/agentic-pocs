import os
from data_processor import get_files, GET_FILES_TOOLS_JSON, get_file_content, GET_FILE_CONTENT_TOOLS_JSON
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import json


load_dotenv(override=True)  # Load environment variables from .env file

system_message = """
You are a tour guide.

Your responsibilities:
- Provide clear and engaging details about tour destinations.
- Destination details are stored in the directory named 'data-files'.
- You have tools to:
  • List the files in the directory
  • Read the content of those files
- Use these tools to gather and present the most relevant information in response to user questions.
- If no information is available, respond with: "I am sorry, I do not have information about that destination."
- Don't provide any other details other than what is given in the data-files.
"""
tools=[{"type": "function", "function": GET_FILES_TOOLS_JSON}, {"type": "function", "function": GET_FILE_CONTENT_TOOLS_JSON}]


def chat(message,history=[]):
    messages=[{"role": "system", "content": system_message}, *history,{"role": "user", "content": message}]
    llm = OpenAI()
    response = llm.chat.completions.create(model="gpt-4o-mini", tools=tools, messages=messages )

    while response.choices[0].finish_reason == "tool_calls":
        tools_result=handle_tool_calls(response.choices[0].message.tool_calls)
        messages.append(response.choices[0].message)
        messages.extend(tools_result)  
        response = llm.chat.completions.create(model="gpt-4o-mini", tools=tools, messages=messages )

    return response.choices[0].message.content

def handle_tool_calls(tool_calls):
    result=[]
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        tool=globals().get(tool_name)
        tool_output=tool(**arguments) if tool else "Unknown tool"
        '''
        if tool_name == "get_files":
            tool_output = get_files("data-files")
        elif tool_name == "get_file_content":
            args = json.loads(tool_input)
            tool_output = get_file_content(args.get("file_path", ""))
        else:
            tool_output = "Unknown tool"
        '''
        result.append({"role": "tool", "content": json.dumps(tool_output), "tool_call_id": tool_call.id})
    return result

def main():
    gr.ChatInterface(fn=chat, title="Tour Guide", description="Ask questions about tour destinations.").launch(inbrowser=True)
main()
