# backend/app/services/ai_service.py
"""
Lógica de negócio para integração com serviços de IA generativa.
"""
import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_text(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text