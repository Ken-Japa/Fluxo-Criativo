import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_text_content(prompt: str) -> dict:
    """
    Gera conteúdo de texto usando o modelo Gemini-Pro.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.

    Returns:
        dict: Um dicionário contendo o conteúdo gerado ou uma mensagem de erro.
    """
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        try:
            generated_content = json.loads(response.text)
        except json.JSONDecodeError:
            generated_content = {"error": "Não foi possível decodificar JSON da resposta da IA", "raw_response": response.text}
        return {"status": "success", "generated_content": generated_content}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_image_description(prompt: str) -> dict:
    """
    Gera uma descrição de imagem/vídeo usando o modelo Gemini-Pro.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.

    Returns:
        dict: Um dicionário contendo a descrição gerada ou uma mensagem de erro.
    """
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        return {"status": "success", "visual_prompt": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}