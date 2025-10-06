import os
import json
from dotenv import load_dotenv
from .prompt_manager import PromptManager
from .utils.cache_manager import get_cache_key, get_from_cache, set_to_cache
from .llm_client.gemini_client import generate_text_content, generate_image_description

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def generate_content_for_client(
    client_profile: dict,
    niche_guidelines: dict,
    content_type: str,
    weekly_themes: list[str],
    weekly_goal: str
) -> dict:
    """
    Gera conteúdo para redes sociais usando a API do Google Gemini, com base nos inputs fornecidos.

    Args:
        client_profile (dict): Dicionário com o perfil do cliente (subnicho, tom_de_voz, publico_alvo, objetivos_gerais).
        niche_guidelines (dict): Dicionário com as diretrizes do nicho (restricoes_conteudo, exemplos_sucesso).
        content_type (str): O tipo de conteúdo a ser gerado (ex: 'instagram_post').
        weekly_themes (list[str]): Uma lista de temas a serem abordados na semana.
        weekly_goal (str): O objetivo principal do conteúdo para a semana.

    Returns:
        dict: Um dicionário contendo o conteúdo gerado, o prompt enviado, informações de tokens e custo.
    """

    # Cria uma chave de cache baseada nos parâmetros do prompt
    cache_key_data = {
        "client_profile": client_profile,
        "niche_guidelines": niche_guidelines,
        "content_type": content_type,
        "weekly_themes": weekly_themes,
        "weekly_goal": weekly_goal
    }
    cache_key = get_cache_key(cache_key_data)

    # Verifica se o resultado está no cache
    if get_from_cache(cache_key):
        print("Retornando resultado do cache.")
        cached_result = get_from_cache(cache_key)
        cached_result["status"] = "success_from_cache"
        return cached_result

    prompt_manager = PromptManager(client_profile, niche_guidelines)
    prompt = prompt_manager.build_prompt(content_type, weekly_themes, weekly_goal)

    # Estima o consumo de tokens
    estimated_tokens = prompt_manager.get_token_count(prompt)
    # Custo estimado (exemplo: $0.0002 por 1K tokens de input para gemini-pro)
    estimated_cost = (estimated_tokens / 1000) * 0.0002

    try:
        response_data = generate_text_content(prompt)
        if response_data.get("status") == "error":
            print(f"Erro ao gerar conteúdo: {response_data.get("message", "Erro desconhecido")}")
            return {
                "status": "error",
                "message": response_data.get("message", "Erro desconhecido"),
                "prompt_sent": prompt,
                "token_usage": {
                    "estimated_input_tokens": estimated_tokens,
                    "estimated_cost_usd": estimated_cost
                }
            }

        if response_data["status"] == "success":
            generated_content = response_data["generated_content"]
        else:
            raise Exception(response_data["message"]) 

        result = {
            "status": "success",
            "generated_content": generated_content,
            "prompt_sent": prompt,
            "token_usage": {
                "estimated_input_tokens": estimated_tokens,
                "estimated_cost_usd": estimated_cost
            }
        }
        set_to_cache(cache_key, result) # Armazena no cache
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "prompt_sent": prompt,
            "token_usage": {
                "estimated_input_tokens": estimated_tokens,
                "estimated_cost_usd": estimated_cost
            }
        }



def generate_image_prompts(post_content: dict, client_profile: dict) -> dict:
    """
    Gera um prompt descritivo para uma IA de geração de imagens/vídeos com base no conteúdo de um post.

    Args:
        post_content (dict): Dicionário contendo o conteúdo de um post (ex: legenda_principal, formato_sugerido).
        client_profile (dict): Dicionário com o perfil do cliente (subnicho, tom_de_voz, publico_alvo).

    Returns:
        dict: Um dicionário contendo o prompt visual gerado, informações de tokens e custo.
    """
    prompt_manager = PromptManager(client_profile, {})
    prompt = prompt_manager.build_image_prompt(post_content)

    estimated_tokens = prompt_manager.get_token_count(prompt)
    estimated_cost = (estimated_tokens / 1000) * 0.0002

    try:
        response_data = generate_image_description(prompt)
        if response_data["status"] == "success":
            visual_prompt = response_data["visual_prompt"]
        else:
            raise Exception(response_data["message"])

        return {
            "status": "success",
            "visual_prompt": visual_prompt,
            "token_usage": {
                "estimated_input_tokens": estimated_tokens,
                "estimated_cost_usd": estimated_cost
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "prompt_sent": prompt,
            "token_usage": {
                "estimated_input_tokens": estimated_tokens,
                "estimated_cost_usd": estimated_cost
            }
        }