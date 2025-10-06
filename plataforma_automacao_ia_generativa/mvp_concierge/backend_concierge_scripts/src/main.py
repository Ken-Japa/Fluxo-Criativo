import os
import json
from datetime import datetime
from dotenv import load_dotenv

from .data_storage import init_db, insert_brief, get_client_profile, insert_client_profile
from .content_generator import generate_content_for_client
from .pdf_generator import create_briefing_pdf
from .html_generator import create_briefing_html
from .utils.briefing_loader import load_briefing_from_json
from .utils.prompt_logger import log_prompt


# backend_concierge_scripts/main.py
"""
Ponto de entrada principal para os scripts de automação do serviço Concierge.
Orquestra as chamadas para os módulos de geração de conteúdo, gerenciamento de prompts e armazenamento de dados.
"""


def main():
    """
    Função principal que orquestra o fluxo de processamento do Concierge MVP.
    Inclui inicialização do DB, coleta de briefing, geração de conteúdo,
    salvamento no DB e geração de PDF.
    """
    print("\n--- Iniciando Concierge MVP ---")

    # 1. Inicializar o Banco de Dados
    print("Inicializando o banco de dados...")
    init_db()
    print("Banco de dados pronto.")

    # 2. Coletar Briefing do Cliente a partir de arquivo JSON
    print("\n--- Coleta de Briefing do Cliente (via JSON) ---")
    briefing_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_briefing.json')
    brief_data = load_briefing_from_json(briefing_filepath)

    if not brief_data:
        print("Não foi possível carregar os dados do briefing. Encerrando.")
        return

    client_name = brief_data.get("client_name", "")
    subniche = brief_data.get("subniche", "")
    contact_info = brief_data.get("contact_info", "")
    public_target = brief_data.get("public_target", "")
    tone_of_voice = brief_data.get("tone_of_voice", "")
    niche_examples = brief_data.get("niche_examples", [])
    content_type = brief_data.get("content_type", "")
    weekly_themes = brief_data.get("weekly_themes", [])
    weekly_goal = brief_data.get("weekly_goal", "")

    if not client_name:
        print("Erro: 'client_name' não encontrado no arquivo de briefing. Encerrando.")
        return

    print(f"Briefing carregado para o cliente: {client_name}")

    # 3. Obter/Criar Perfil do Cliente
    print(f"\nVerificando perfil para '{client_name}'...")
    client_profile = get_client_profile(client_name)

    if not client_profile:
        print(f"Perfil para '{client_name}' não encontrado. Criando novo perfil...")
        insert_client_profile(
            client_name=client_name,
            contact_info=contact_info,
            public_target=public_target,
            tone_of_voice=tone_of_voice,
            niche_examples=niche_examples,
            status='active'
        )
        client_profile = get_client_profile(client_name) # Recupera o perfil recém-criado
        print("Novo perfil de cliente criado.")
    else:
        print(f"Perfil para '{client_name}' encontrado. Usando perfil existente.")

    # 4. Gerar Conteúdo
    print("\n--- Gerando Conteúdo para Redes Sociais ---")
    try:
        # generate_content_for_client espera dicionários para profile e guidelines
        generated_data = generate_content_for_client(
            client_profile=brief_data, # Usando brief_data como client_profile para este exemplo
            niche_guidelines={"subniche": subniche, "examples": niche_examples},
            content_type=content_type,
            weekly_themes=weekly_themes,
            weekly_goal=weekly_goal
        )
        generated_content = generated_data["generated_content"]
        prompt_used_for_content_generation = generated_data["prompt_sent"]
        tokens_consumed = generated_data["token_usage"]["estimated_input_tokens"]
        api_cost_usd = generated_data["token_usage"]["estimated_cost_usd"]
        print("Conteúdo gerado com sucesso!")

        # Log do prompt utilizado
        log_prompt(client_name, prompt_used_for_content_generation, "content_generation")

    except Exception as e:
        print(f"Erro ao gerar conteúdo: {e}")
        return

    # 5. Salvar Briefing e Conteúdo no Banco de Dados
    print("\nSalvando briefing e conteúdo no banco de dados...")
    delivery_date = datetime.now().strftime('%Y-%m-%d')
    insert_brief(
        client_name=client_name,
        subniche=subniche,
        brief_data=brief_data,
        generated_content=generated_content,
        prompt_used=prompt_used_for_content_generation,
        tokens_consumed=tokens_consumed,
        api_cost_usd=api_cost_usd,
        delivery_date=delivery_date
    )
    print("Briefing e conteúdo salvos no DB.")

    # 6. Gerar PDF
    print("\n--- Gerando PDF do Briefing ---")
    output_pdf_filename = f"briefing_{client_name.replace(' ', '_')}_{delivery_date}.pdf"
    try:
        create_briefing_pdf(generated_content, client_name, output_pdf_filename)
        print(f"PDF do briefing gerado em: {output_pdf_filename}")
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return

    # 7. Gerar HTML
    print("\n--- Gerando Relatório HTML ---")
    output_html_filename = f"briefing_{client_name.replace(' ', '_')}_{delivery_date}.html"
    try:
        create_briefing_html(generated_content, client_name, output_html_filename)
        print(f"Relatório HTML gerado em: {output_html_filename}")
    except Exception as e:
        print(f"Erro ao gerar HTML: {e}")
        return

    # 8. Mensagem de Sucesso
    print("\n--- Processamento Concluído com Sucesso! ---")
    print(f"Caminho do PDF gerado: {os.path.abspath(output_pdf_filename)}")
    print(f"Custo estimado da API para esta geração: ${api_cost_usd:.4f}")
    print("------------------------------------------")

if __name__ == "__main__":
    main()