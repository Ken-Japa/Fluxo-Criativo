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
    model = genai.GenerativeModel('gemini-2.5-pro')
    try:
        response = model.generate_content(prompt)
        try:
            # Remove os delimitadores de bloco de código Markdown se presentes
            json_string = response.text.strip()
            if json_string.startswith('```json') and json_string.endswith('```'):
                json_string = json_string[len('```json'):-len('```')].strip()
            
            generated_content = json.loads(json_string)
            return {"status": "success", "generated_content": generated_content}
        except json.JSONDecodeError:
            return {"status": "error", "message": f"Não foi possível decodificar JSON da resposta da IA: {response.text}"}
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