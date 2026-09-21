import os
import requests
from bs4 import BeautifulSoup
URL = "https://getautoseo.com/"

page = requests.get(URL, timeout=20)
page.raise_for_status()

soup = BeautifulSoup(page.text, "html.parser")

text = soup.get_text(" ", strip=True)

print(text[:5000])

api_key = os.environ["OPENROUTER_API_KEY"]

prompt = f"""
Проанализируй компанию по тексту её сайта.

Сайт:
{URL}

Текст сайта:
{text}

Определи:

1. Название компании.
2. Что именно компания продаёт или предлагает.
3. Основные продукты и услуги.
4. Кто является клиентом компании.
5. Какие задачи клиента решают её продукты или услуги.
6. Какие признаки характерны для потенциального клиента.
7. В каком сегменте рынка работает компания.

Для каждого вывода отделяй информацию,
которая прямо подтверждается сайтом,
от предположений.

Ответ дай на русском языке.
"""

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
                "content": prompt
            }
        ],
    },
    timeout=60,
)

response.raise_for_status()

result = response.json()

print(result["choices"][0]["message"]["content"])
