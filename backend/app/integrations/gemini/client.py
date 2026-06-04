import google.generativeai as genai

from app.config import settings


class GeminiClient:
    def __init__(self) -> None:
        genai.configure(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model
        self._model = genai.GenerativeModel(self.model_name)

    async def generate_text(self, prompt: str) -> str:
        response = await self._model.generate_content_async(prompt)
        return response.text or ""
