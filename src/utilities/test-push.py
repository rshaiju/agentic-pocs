import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Your Pushbullet Access Token (get it from https://www.pushbullet.com/#settings)
ACCESS_TOKEN = os.getenv("PUSHBULLET_API_KEY")

# API endpoint
url = "https://api.pushbullet.com/v2/pushes"

# Notification payload
data = {
    "type": "note",          # 'note' is a simple text notification
    "title": "Hello!",       # Notification title
    "body": "This is a test push from Python."  # Notification body
}

# Send the request
response = requests.post(url, json=data, headers={
    "Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
})

# Check result
if response.status_code == 200:
    print("Push sent successfully!")
else:
    print("Error:", response.text)
