import os

import requests
from dotenv import load_dotenv

load_dotenv(override=True)  # Load environment variables from .env file

system_msg = "You are a helpful assistant. You tell fun facts about the world. You are very concise and only respond with the fun fact. You do not provide any other information."

get_response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    json={
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": "Tell me a fun fact about the India."},
        ],
    },
    headers={
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    },
)
if get_response.status_code == 200:
    print(get_response.json()["choices"][0]["message"]["content"])
