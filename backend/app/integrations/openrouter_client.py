import requests

from app.config import settings


class OpenRouterClient:
    def __init__(self) -> None:
        self.api_key = settings.openrouter_api_key
        self.model_name = "deepseek/deepseek-r1-0528:free"

    async def generate_text(self, prompt: str) -> str:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60,
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]