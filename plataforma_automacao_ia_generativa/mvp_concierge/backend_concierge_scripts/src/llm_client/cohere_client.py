import os
import json
import re
from dotenv import load_dotenv
import cohere

load_dotenv()

def consolidar_posts(json1: dict, json2: dict) -> dict:
    """
    Consolida dois JSONs de posts em um único JSON otimizado usando a Cohere.
    Args:
        json1 (dict): Primeiro JSON com 5 ideias de posts.
        json2 (dict): Segundo JSON com 5 ideias de posts.
    Returns:
        dict: JSON consolidado com as 5 melhores ideias ou mensagem de erro.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))

    prompt = f"""
    Você é um especialista em marketing digital e criação de conteúdo para redes sociais.
    Sua tarefa é consolidar os dois JSONs abaixo em um único JSON com as 5 melhores ideias de posts.
    Siga estas regras:
    1. Selecione as 5 ideias mais originais, variadas e alinhadas com o público-alvo.
    2. Mescle ideias similares, melhorando o texto, as hashtags e a estrutura.
    3. Otimize o texto de cada post para engajamento, clareza e adequação ao tom de voz.
    4. Garanta que cada post tenha: título, texto (até 280 caracteres), hashtags e tipo de mídia sugerida.
    5. Retorne apenas o JSON consolidado, sem comentários ou formatação adicional.

    JSON 1: {json.dumps(json1, ensure_ascii=False)}
    JSON 2: {json.dumps(json2, ensure_ascii=False)}
    """
    try:
        response = co.chat(
            model="command-r-plus",
            message=prompt,
            temperature=0.3  # Menor temperatura para respostas mais consistentes
        )
        # Remove marcações de code block se houver
        json_string = re.sub(r"```json\n|```", "", response.text.strip())
        consolidated_json = json.loads(json_string)
        return {"status": "success", "consolidated_content": consolidated_json}
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"Erro ao decodificar JSON: {e}. Resposta bruta: {response.text}"}
    except Exception as e:
        return {"status": "error", "message": f"Erro ao consolidar posts: {e}"}
