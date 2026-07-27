from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)  # Load environment variables from .env file


class Solutioner:
    system_msg = "You are a helpful assistant who can propose solutions for the given business domain and pain point. Please respond with the most suitable solution alone."
    user_msg_prefix = "Please propose the most suitable solution for the below business domain and pain point"

    def __init__(self):
        self.llm = OpenAI()

    def propose_solution(self, user_msg: str):
        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_msg},
                {"role": "user", "content": f"{self.user_msg_prefix}: {user_msg}"},
            ],
        )
        return response.choices[0].message.content
