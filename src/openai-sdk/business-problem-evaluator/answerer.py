from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)  # Load environment variables from .env file


class Answerer:
    system_msg = "You are a helpful assistant who is an expert at identifying the pain points in the given business domain where agentic solutions can be applied. Please respond with the most critical pain point alone."
    user_msg_prefix = (
        "Please identify the most critical pain point in the below business domain"
    )

    def __init__(self):
        self.llm = OpenAI()

    def answer(self, user_msg: str):
        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_msg},
                {"role": "user", "content": f"{self.user_msg_prefix}: {user_msg}"},
            ],
        )
        return response.choices[0].message.content
