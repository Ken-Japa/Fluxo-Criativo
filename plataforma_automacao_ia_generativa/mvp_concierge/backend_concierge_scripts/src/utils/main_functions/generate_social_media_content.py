import os
from src.content_generator import generate_content_for_client
from src.utils.prompt_logger import log_prompt

def generate_social_media_content(brief_data, nome_do_cliente, tipo_de_conteudo, conteudos_semanais, objetivos_de_marketing):
    """
    Gera conteúdo para redes sociais com base nos dados do briefing do cliente.

    Args:
        brief_data (dict): Dados completos do briefing do cliente.
        nome_do_cliente (str): Nome do cliente.
        tipo_de_conteudo (str): Tipo de conteúdo a ser gerado.
        conteudos_semanais (list): Lista de dicionários com os objetivos de conteúdo semanais.
        objetivos_de_marketing (str): Objetivos gerais de marketing.

    Returns:
        tuple: Uma tupla contendo (generated_content, prompt_used_for_content_generation, tokens_consumed, api_cost_usd)
               se o conteúdo for gerado com sucesso, caso contrário, retorna None para todos os valores.
    """
    print("\n--- Gerando Conteúdo para Redes Sociais ---")
    try:
        weekly_themes_list = [item.get("objetivo_do_conteudo_individual", "") for item in conteudos_semanais]
        campaign_type = brief_data.get("tipo_de_campanha", "lancamento")

        client_data = {
            "nome_do_cliente": nome_do_cliente,
            "informacoes_de_contato": brief_data.get("informacoes_de_contato"),
            "publico_alvo": brief_data.get("publico_alvo"),
            "tom_de_voz": brief_data.get("tom_de_voz"),
            "exemplos_de_nicho": brief_data.get("exemplos_de_nicho"),
            "estilo_de_comunicacao": brief_data.get("estilo_de_comunicacao"),
            "vocabulario_da_marca": brief_data.get("vocabulario_da_marca")
        }

        niche_data = {
            "subnicho": brief_data.get("subnicho"),
            "exemplos_de_nicho": brief_data.get("exemplos_de_nicho")
        }

        generated_data = generate_content_for_client(
            client_data=client_data,
            niche_data=niche_data,
            weekly_themes=weekly_themes_list,
            weekly_goal=objetivos_de_marketing,
            campaign_type=campaign_type
        )

        if generated_data.get("status") == "error":
            print(f"Erro ao gerar conteúdo: {generated_data.get("message", "Erro desconhecido")}")
            return None, None, None, None

        generated_content = generated_data["generated_content"]
        prompt_used_for_content_generation = generated_data["prompt_sent"]
        tokens_consumed = generated_data["token_usage"]["estimated_input_tokens"]
        api_cost_usd = generated_data["token_usage"]["estimated_cost_usd"]
        print("Conteúdo gerado com sucesso!")

        # Log do prompt utilizado
        log_prompt(nome_do_cliente, prompt_used_for_content_generation, "content_generation")
        
        return generated_content, prompt_used_for_content_generation, tokens_consumed, api_cost_usd

    except Exception as e:
        print(f"Erro ao gerar conteúdo: {e}")
        return None, None, None, None