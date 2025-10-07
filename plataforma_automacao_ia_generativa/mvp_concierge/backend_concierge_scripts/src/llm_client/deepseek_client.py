import os
import json
import re
import requests # Adicionado para requisições HTTP
from dotenv import load_dotenv

load_dotenv()

def generate_text_content(prompt: str) -> dict:
    """
    Gera conteúdo de texto usando o modelo DeepSeek-Chat via OpenRouter.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.

    Returns:
        dict: Um dicionário contendo o conteúdo gerado ou uma mensagem de erro.
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    api_url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        
        response_json = response.json()
        generated_content = response_json['choices'][0]['message']['content']
        
        # Tenta decodificar o conteúdo gerado se for uma string JSON
        try:
            parsed_content = json.loads(generated_content)
            return {"status": "success", "generated_content": parsed_content}
        except json.JSONDecodeError:
            # Se não for um JSON válido, retorna como texto simples
            return {"status": "success", "generated_content": generated_content}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Erro na requisição HTTP para DeepSeek via OpenRouter: {e}"}
    except KeyError as e:
        return {"status": "error", "message": f"Estrutura de resposta inesperada da API DeepSeek: {e}. Resposta bruta: {response_json}"}
    except Exception as e:
        return {"status": "error", "message": f"Erro inesperado ao gerar conteúdo de texto com DeepSeek: {e}"}

def generate_image_description(prompt: str) -> dict:
    """
    Gera uma descrição de imagem/vídeo usando o modelo DeepSeek-Chat via OpenRouter.
    (Nota: DeepSeek não possui um modelo específico para descrição de imagem como o Gemini,
    então usaremos o modelo de chat para gerar texto baseado no prompt.)

    Args:
        prompt (str): O prompt a ser enviado para o modelo.

    Returns:
        dict: Um dicionário contendo a descrição gerada ou uma mensagem de erro.
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    api_url = 'https://openrouter.ai/api/v1/chat/completions'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        
        response_json = response.json()
        visual_prompt = response_json['choices'][0]['message']['content']
        
        return {"status": "success", "visual_prompt": visual_prompt}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Erro na requisição HTTP para DeepSeek via OpenRouter: {e}"}
    except KeyError as e:
        return {"status": "error", "message": f"Estrutura de resposta inesperada da API DeepSeek: {e}. Resposta bruta: {response_json}"}
    except Exception as e:
        return {"status": "error", "message": f"Erro inesperado ao gerar descrição de imagem com DeepSeek: {e}"}