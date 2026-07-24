from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)  # Load environment variables from .env file

class BaseAgent:
    def __init__(self, system_msg: str = "You are a helpful assistant"):
        self.llm = OpenAI() 
        self.system_msg = system_msg

    def chat(self, user_msg: str):
        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_msg},
                {"role": "user", "content": user_msg}
            ])
        return response.choices[0].message.content

        