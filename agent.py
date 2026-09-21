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
"customer_examples": [],
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

2. В "products_and_services" помещай ТОЛЬКО продукты и услуги, которые сама анализируемая компания непосредственно предлагает или продаёт.

3. НЕ помещай в "products_and_services":
   - статьи из блога;
   - темы опубликованных материалов;
   - примеры контента;
   - кейсы клиентов;
   - названия компаний-клиентов;
   - партнёрские компании;
   - сторонние продукты и сервисы;
   - демонстрационные проекты.

4. В "customer_examples" помещай компании или людей, которые на сайте представлены как клиенты, пользователи, заказчики или участники case study.

5. Если компания просто упоминается в статье, примере, демонстрации или стороннем материале, НЕ считай её клиентом.

6. В "use_cases" описывай реальные задачи, для решения которых сама компания предлагает свои продукты или услуги.

7. Не превращай отдельный пример статьи или кейс в отдельную отрасль целевого рынка.

8. В "icp" указывай только признаки потенциального клиента, которые подтверждаются сайтом. Если признак является логическим выводом, помещай его в "hypotheses".

9. В "buyer_roles" указывай должности людей, которые могут принимать решение о покупке продукта. Не утверждай конкретного ЛПР без подтверждения.

10. В "evidence" указывай конкретные факты из сайта, подтверждающие выводы.

11. В "hypotheses" помещай только выводы, которые являются предположениями.

12. Не придумывай факты, которых нет в тексте.

13. Если информации недостаточно, оставляй массив пустым.

14. Верни ТОЛЬКО JSON без пояснений, Markdown и ```.

15. Ответ должен быть валидным JSON.
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
