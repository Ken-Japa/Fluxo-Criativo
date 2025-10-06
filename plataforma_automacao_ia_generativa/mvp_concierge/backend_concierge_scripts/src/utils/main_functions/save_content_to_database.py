import json
from datetime import datetime
from src.data_storage import insert_brief

def save_content_to_database(brief_data, nome_do_cliente, generated_content, prompt_used_for_content_generation, tokens_consumed, api_cost_usd):
    """
    Salva os dados do briefing e o conteúdo gerado no banco de dados.

    Args:
        brief_data (dict): Dados completos do briefing do cliente.
        nome_do_cliente (str): Nome do cliente.
        generated_content (str): Conteúdo gerado para as redes sociais.
        prompt_used_for_content_generation (str): O prompt usado para gerar o conteúdo.
        tokens_consumed (int): Número de tokens consumidos na geração do conteúdo.
        api_cost_usd (float): Custo estimado da API em USD.
    """
    print("\n--- Salvando Conteúdo no Banco de Dados ---")
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        subniche = brief_data.get('subniche', 'N/A') # Assumindo que 'subniche' está em brief_data
        briefing_id = insert_brief(
            client_name=nome_do_cliente,
            subniche=subniche,
            brief_data=brief_data,
            generated_content=generated_content, # Removido json.loads()
            prompt_used=prompt_used_for_content_generation,
            tokens_consumed=tokens_consumed,
            api_cost_usd=api_cost_usd,
            delivery_date=timestamp
        )
        print("Briefing e conteúdo salvos no banco de dados com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar briefing e conteúdo no banco de dados: {e}")