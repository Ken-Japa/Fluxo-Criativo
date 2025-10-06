import os
import json
import time

from ...prompt_manager import PromptManager
from ..cache_manager import get_cache_key, get_from_cache, set_to_cache
from ..llm_client.gemini_client import generate_text_content



def generate_content_for_client(
    client_profile: dict,
    content_type: str,
    weekly_themes: list[str],
    weekly_goal: str
) -> dict:
    """
    Gera conteúdo para redes sociais usando a API do Google Gemini, com base nos inputs fornecidos.

    Args:
        client_profile (dict): Dicionário com o perfil do cliente (subnicho, tom_de_voz, publico_alvo, objetivos_gerais).
        content_type (str): O tipo de conteúdo a ser gerado (ex: 'instagram_post').
        weekly_themes (list[str]): Uma lista de temas a serem abordados na semana.
        weekly_goal (str): O objetivo principal do conteúdo para a semana.

    Returns:
        dict: Um dicionário contendo o conteúdo gerado, o prompt enviado, informações de tokens e custo.
    """

    # Cria uma chave de cache baseada nos parâmetros do prompt
    cache_key_data = {
        "client_profile": client_profile,
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

    prompt_manager = PromptManager(client_profile)

    # Realiza a análise estratégica inicial
    strategic_analysis_result = prompt_manager.analyze_briefing_for_strategy(
        client_profile=client_profile,
        niche_guidelines=client_profile.get("niche_guidelines")
    )

    prompt = prompt_manager.build_prompt(
        content_type,
        weekly_themes,
        weekly_goal,
        strategic_analysis=strategic_analysis_result
    )

    # Estima o consumo de tokens
    estimated_tokens = prompt_manager.get_token_count(prompt)
    # Custo estimado (exemplo: $0.0002 por 1K tokens de input para gemini-pro)
    estimated_cost = (estimated_tokens / 1000) * 0.0002

    max_retries = 3
    base_delay = 1  # segundos

    for attempt in range(max_retries):
        try:
            response_data = generate_text_content(prompt)
            if response_data.get("status") == "error":
                error_message = response_data.get("message", "Erro desconhecido ao chamar a API Gemini.")
                print(f"Erro ao gerar conteúdo: {error_message}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Tentando novamente em {delay} segundos...")
                    time.sleep(delay)
                    continue
                else:
                    return {
                        "status": "error",
                        "message": f"Falha na geração de conteúdo pela API Gemini após {max_retries} tentativas: {error_message}",
                        "prompt_sent": prompt,
                        "token_usage": {
                            "estimated_input_tokens": estimated_tokens,
                            "estimated_cost_usd": estimated_cost
                        }
                    }

            if response_data["status"] == "success":
                raw_content = response_data["generated_content"]
                # Tenta extrair o JSON de um bloco de código markdown
                json_start = raw_content.find("```json")
                json_end = raw_content.rfind("```")

                if json_start != -1 and json_end != -1 and json_start < json_end:
                    json_string = raw_content[json_start + len("```json"):json_end].strip()
                else:
                    # Fallback: tenta encontrar o JSON bruto
                    json_start = raw_content.find("{")
                    json_end = raw_content.rfind("}")
                    if json_start != -1 and json_end != -1 and json_start < json_end:
                        json_string = raw_content[json_start : json_end + 1].strip()
                    else:
                        # Se não encontrar JSON em bloco de código nem bruto, tenta extrair a primeira e última chaves
                        json_string = raw_content.strip()
                        if not (json_string.startswith("{") and json_string.endswith("}")):
                            raise ValueError("Não foi possível encontrar uma estrutura JSON válida na resposta da IA.")

                try:
                    generated_content = json.loads(json_string)
                except json.JSONDecodeError as e:
                    print(f"Erro de decodificação JSON: {e}")
                    print(f"Conteúdo JSON bruto que causou o erro: {json_string}")
                    raise ValueError(f"Erro ao decodificar JSON da resposta da IA: {e}\nConteúdo bruto: {json.dumps(json_string)}")
                
                # Validação básica da estrutura JSON esperada (ex: verificar se 'weekly_strategy_summary' existe)
                if "weekly_strategy_summary" not in generated_content:
                    raise ValueError("A resposta JSON não contém a chave 'weekly_strategy_summary' esperada.")
                
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
            else:
                # Se o status não for 'success' e não for 'error' (o que já foi tratado), levanta uma exceção
                raise Exception(response_data.get("message", "Resposta inesperada da API Gemini."))

        except Exception as e:
            print(f"Exceção durante a chamada da API Gemini (tentativa {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                return {
                    "status": "error",
                    "message": f"Falha na geração de conteúdo pela API Gemini após {max_retries} tentativas: {str(e)}",
                    "prompt_sent": prompt,
                    "token_usage": {
                        "estimated_input_tokens": estimated_tokens,
                        "estimated_cost_usd": estimated_cost
                    }
                }