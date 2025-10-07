import os
import json
import re
from datetime import datetime
from src.content_generator import generate_content_for_client
from src.utils.prompt_logger import log_prompt

def _sanitize_filename(filename):
    """
    Sanitiza uma string para ser usada como nome de arquivo.
    Remove caracteres inválidos e limita o comprimento.
    """
    # Substitui caracteres inválidos por underscore
    filename = re.sub(r'[<>:"/\\|?*\s]+', '_', filename)
    # Remove underscores duplicados
    filename = re.sub(r'_+', '_', filename)
    # Remove underscores do início e fim
    filename = filename.strip('_')
    # Limita o comprimento do nome do arquivo para evitar problemas de sistema de arquivos
    return filename[:100]

def generate_social_media_content(brief_data, nome_do_cliente, tipo_de_conteudo, conteudos_semanais, objetivos_de_marketing, output_dir):
    """
    Gera conteúdo para redes sociais com base nos dados do briefing do cliente, usando Gemini e DeepSeek.

    Args:
        brief_data (dict): Dados completos do briefing do cliente.
        nome_do_cliente (str): Nome do cliente.
        tipo_de_conteudo (str): Tipo de conteúdo a ser gerado.
        conteudos_semanais (list): Lista de dicionários com os objetivos de conteúdo semanais.
        objetivos_de_marketing (str): Objetivos gerais de marketing.

    Returns:
        tuple: Uma tupla contendo (gemini_generated_content, deepseek_generated_content, prompt_used_for_content_generation, tokens_consumed_gemini, api_cost_usd_gemini, tokens_consumed_deepseek, api_cost_usd_deepseek)
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
            "vocabulario_da_marca": brief_data.get("vocabulario_da_marca"),
            "canais_de_distribuicao": brief_data.get("canais_de_distribuicao"),
            "subnicho": brief_data.get("subnicho"),
            "analise_swot": brief_data.get("analise_swot"),
            "publico_alvo_detalhado": brief_data.get("publico_alvo_detalhado"),
            "objetivos_de_marketing": brief_data.get("objetivos_de_marketing"),
            "topicos_principais": brief_data.get("topicos_principais"),
            "palavras_chave": brief_data.get("palavras_chave"),
            "chamada_para_acao": brief_data.get("chamada_para_acao"),
            "restricoes_e_diretrizes": brief_data.get("restricoes_e_diretrizes"),
            "informacoes_adicionais": brief_data.get("informacoes_adicionais"),
            "referencias_de_estilo_e_formato": brief_data.get("referencias_de_estilo_e_formato")
        }

        niche_data = {
            "subnicho": brief_data.get("subnicho"),
            "exemplos_de_nicho": brief_data.get("exemplos_de_nicho"),
            "analise_de_concorrentes_referencias": brief_data.get("analise_de_concorrentes_referencias")
        }

        # # Gerar conteúdo com Gemini
        # print("Gerando conteúdo com Gemini...")
        # gemini_generated_data = generate_content_for_client(
        #     client_data=client_data,
        #     niche_data=niche_data,
        #     weekly_themes=weekly_themes_list,
        #     weekly_goal=objetivos_de_marketing,
        #     campaign_type=campaign_type,
        #     content_type=tipo_de_conteudo,
        #     use_deepseek=False
        # )

        # if gemini_generated_data.get("status") == "error":
        #     print(f"Erro ao gerar conteúdo com Gemini: {gemini_generated_data.get("message", "Erro desconhecido")}")
        #     return None, None, None, None, None, None, None

        # gemini_content = gemini_generated_data["generated_content"]
        # prompt_used_for_content_generation = gemini_generated_data["prompt_sent"]
        # tokens_consumed_gemini = gemini_generated_data["token_usage"]["estimated_input_tokens"]
        # api_cost_usd_gemini = gemini_generated_data["token_usage"]["estimated_cost_usd"]
        # print("Conteúdo Gemini gerado com sucesso!")

        # # Salvar JSON do Gemini
        # output_dir = os.path.join(os.getcwd(), "output_files", "respostas_IA")
        # os.makedirs(output_dir, exist_ok=True)
        # gemini_output_path = os.path.join(output_dir, f"Gemini-{nome_do_cliente}-{tipo_de_conteudo}.json")
        # with open(gemini_output_path, "w", encoding="utf-8") as f:
        #     json.dump(gemini_content, f, ensure_ascii=False, indent=4)
        # print(f"Conteúdo Gemini salvo em: {gemini_output_path}")

        # Gerar conteúdo com DeepSeek
        print("Gerando conteúdo com DeepSeek...")
        deepseek_generated_data = generate_content_for_client(
            client_data=client_data,
            niche_data=niche_data,
            weekly_themes=weekly_themes_list,
            weekly_goal=objetivos_de_marketing,
            campaign_type=campaign_type,
            content_type=tipo_de_conteudo,
            use_deepseek=True
        )

        if deepseek_generated_data.get("status") == "error":
            print(f"Erro ao gerar conteúdo com DeepSeek: {deepseek_generated_data.get("message", "Erro desconhecido")}")
            return None, None, None, None, None, None, None

        deepseek_content = deepseek_generated_data["generated_content"]
        prompt_used_for_content_generation = deepseek_generated_data["prompt_sent"]
        tokens_consumed_deepseek = deepseek_generated_data["token_usage"]["estimated_input_tokens"]
        api_cost_usd_deepseek = deepseek_generated_data["token_usage"]["estimated_cost_usd"]
        print("Conteúdo DeepSeek gerado com sucesso!")

        # Salvar JSON do DeepSeek
        sanitized_client_name = _sanitize_filename(nome_do_cliente)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deepseek_output_path = os.path.join(output_dir, f"Deepseek-{sanitized_client_name}_{timestamp}.json")
        with open(deepseek_output_path, "w", encoding="utf-8") as f:
            json.dump(deepseek_content, f, ensure_ascii=False, indent=4)
        print(f"Conteúdo DeepSeek salvo em: {deepseek_output_path}")

        print("Conteúdo gerado com sucesso por DeepSeek!")

        # Log do prompt utilizado (o prompt é o mesmo para ambas as IAs)
        log_prompt(nome_do_cliente, prompt_used_for_content_generation, "content_generation")
        
        return None, deepseek_content, prompt_used_for_content_generation, None, None, tokens_consumed_deepseek, api_cost_usd_deepseek

    except Exception as e:
        print(f"Erro ao gerar conteúdo: {e}")
        return None, None, None, None, None, None, None