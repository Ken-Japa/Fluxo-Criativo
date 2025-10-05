# backend/app/core/config.py
"""
Configurações da aplicação, variáveis de ambiente e dependências.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Plataforma de Automação de Conteúdo com IA Generativa"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    GOOGLE_API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()