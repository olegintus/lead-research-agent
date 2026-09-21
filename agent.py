import os
import requests
from bs4 import BeautifulSoup

api_key = os.environ["OPENROUTER_API_KEY"]

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "inclusionai/ling-3.0-flash-fin:free",
        "messages": [
            {
                "role": "user",
                "content": "Ответь одним словом: работает?"
            }
        ],
    },
)

print(response.status_code)
print(response.text)
