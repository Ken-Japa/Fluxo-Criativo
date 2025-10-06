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
    max_retries = 3
    base_delay = 1  # segundos

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            try:
                # Remove os delimitadores de bloco de código Markdown se presentes
                json_string = response.text.strip()
                if json_string.startswith('```json') and json_string.endswith('```'):
                    json_string = json_string[len('```json'):-len('```')].strip()
                
                generated_content = json.loads(json_string)
                return {"status": "success", "generated_content": generated_content}
            except json.JSONDecodeError as e:
                return {"status": "error", "message": f"Erro de decodificação JSON na resposta da IA: {e}. Resposta bruta: {response.text}"}
        except google.api_core.exceptions.GoogleAPIError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Erro da API Google Gemini (tentativa {attempt + 1}): {e}. Tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                return {"status": "error", "message": f"Falha na API Google Gemini após {max_retries} tentativas: {e}"}
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
    max_retries = 3
    base_delay = 1  # segundos

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return {"status": "success", "visual_prompt": response.text}
        except google.api_core.exceptions.GoogleAPIError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Erro da API Google Gemini ao gerar descrição de imagem (tentativa {attempt + 1}): {e}. Tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                return {"status": "error", "message": f"Falha na API Google Gemini ao gerar descrição de imagem após {max_retries} tentativas: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"Erro inesperado ao gerar descrição de imagem: {e}"}