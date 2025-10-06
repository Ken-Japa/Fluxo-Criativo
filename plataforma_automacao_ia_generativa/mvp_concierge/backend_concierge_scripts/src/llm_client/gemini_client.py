import os
import json
import time
import google.generativeai as genai
import google.api_core.exceptions
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
        print(f"DEBUG: response.text type: {type(response.text)}")
        print(f"DEBUG: response.text content: {response.text[:500]}") # Print first 500 chars
        try:
            # Remove os delimitadores de bloco de código Markdown se presentes
            json_string = response.text.strip()
            if json_string.startswith('```json') and json_string.endswith('```'):
                json_string = json_string[len('```json'):-len('```')].strip()
            
            print(f"DEBUG: json_string type: {type(json_string)}")
            print(f"DEBUG: json_string content: {json_string[:500]}") # Print first 500 chars

            generated_content = json.loads(json_string)
            return {"status": "success", "generated_content": generated_content}
        except json.JSONDecodeError as e:
            return {"status": "error", "message": f"Erro de decodificação JSON na resposta da IA: {e}. Resposta bruta: {response.text}"}
    except google.api_core.exceptions.GoogleAPIError as e:
        return {"status": "error", "message": f"Falha na API Google Gemini: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Erro inesperado ao gerar conteúdo de texto: {e}"}

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
    except google.api_core.exceptions.GoogleAPIError as e:
        return {"status": "error", "message": f"Falha na API Google Gemini ao gerar descrição de imagem: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Erro inesperado ao gerar descrição de imagem: {e}"}