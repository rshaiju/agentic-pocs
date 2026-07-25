from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)  # Load environment variables from .env file

class BusinessDomainProposer:
    system_msg = "You are a helpful assistant who can propose a business domains for applying agentic solutions. Please respond with the name of the business domain alone." \
    
    def __init__(self):
        self.llm = OpenAI() 

    def propose(self, user_msg: str):
        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_msg},
                {"role": "user", "content": user_msg}
            ])
        return response.choices[0].message.content