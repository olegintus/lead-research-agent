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

Верни результат СТРОГО в формате JSON.

Структура JSON:

{{
  "company": {{
    "name": "",
    "website": "",
    "description": ""
  }},
  "products_and_services": [],
  "customers": [],
  "use_cases": [],
  "icp": {{
    "industries": [],
    "company_types": [],
    "company_size": [],
    "geography": [],
    "characteristics": []
  }},
  "buyer_roles": [],
  "market": [],
  "evidence": [],
  "hypotheses": []
}}

Правила:

1. Используй только информацию из текста сайта.
2. Не придумывай факты, которых нет в тексте.
3. В "evidence" указывай конкретные факты с сайта, подтверждающие выводы.
4. В "hypotheses" помещай только выводы, которые являются предположениями.
5. Если информации недостаточно, оставляй массив пустым.
6. "buyer_roles" — предполагаемые должности лиц, принимающих решение о покупке.
7. Верни ТОЛЬКО JSON без пояснений, Markdown и ```.

Ответ должен быть валидным JSON.
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

import json
import re

result = response.json()

content = result["choices"][0]["message"]["content"]

content = re.sub(r"^```json\s*", "", content.strip())
content = re.sub(r"\s*```$", "", content)

data = json.loads(content)

print(json.dumps(data, ensure_ascii=False, indent=2))
