# backend/main.py
"""
Ponto de entrada principal para a API FastAPI do SaaS.
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do SaaS de Automação de Conteúdo!"}