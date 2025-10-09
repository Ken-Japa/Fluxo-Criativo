import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def generate_text_content(prompt: str) -> dict:
    """
    Gera conteúdo de texto usando o modelo da Mistral AI.
    Args:
        prompt (str): O prompt a ser enviado para o modelo.
    Returns:
        dict: Um dicionário contendo o conteúdo gerado ou uma mensagem de erro.
    """
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    try:
        response = client.chat(
            model="mistral-large-latest",  # ou outro modelo disponível
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            # Remove marcações de code block se houver
            json_string = re.sub(r"```json\n|```", "", response.choices[0].message.content.strip())
            generated_content = json.loads(json_string)
            return {"status": "success", "generated_content": generated_content}
        except json.JSONDecodeError as e:
            return {"status": "error", "message": f"Erro de decodificação JSON na resposta da IA: {e}. Resposta bruta: {response.choices[0].message.content}"}
    except Exception as e:
        return {"status": "error", "message": f"Erro ao gerar conteúdo de texto: {e}"}

def generate_image_description(prompt: str) -> dict:
    """
    Gera uma descrição de imagem/vídeo usando o modelo da Mistral AI.
    Args:
        prompt (str): O prompt a ser enviado para o modelo.
    Returns:
        dict: Um dicionário contendo a descrição gerada ou uma mensagem de erro.
    """
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    try:
        response = client.chat(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"status": "success", "visual_prompt": response.choices[0].message.content}
    except Exception as e:
        return {"status": "error", "message": f"Erro ao gerar descrição de imagem: {e}"}
