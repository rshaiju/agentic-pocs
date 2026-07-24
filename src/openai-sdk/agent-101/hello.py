from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)  # Load environment variables from .env file

system_msg = "You are a helpful assistant"
user_msg = "Hello, how are you?"

llm = OpenAI()

response = llm.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
    ])

print(response.choices[0].message.content)