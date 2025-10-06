import os
import json
from datetime import datetime
from dotenv import load_dotenv

from src.data_storage import init_db, insert_brief, get_client_profile, get_all_briefs, insert_client_profile
from src.content_generator import generate_content_for_client
from src.pdf_generator import create_briefing_pdf
from src.html_generator import create_briefing_html
from src.utils.briefing_loader import load_briefing_from_json
from src.utils.prompt_logger import log_prompt
from src.config import COMPANY_NAME, BASE_DIR


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

def validate_briefing_data(brief_data: dict):
    """
    Valida os dados do briefing do cliente para garantir que todos os campos obrigatórios estejam presentes
    e com os tipos corretos.

    Args:
        brief_data (dict): Dicionário contendo os dados do briefing do cliente.

    Raises:
        ValueError: Se algum campo obrigatório estiver faltando ou for inválido.
    """
    required_fields = {
        "nome_do_cliente": str,
        "subnicho": str,
        "publico_alvo": str,
        "tom_de_voz": str,
        "objetivos_de_marketing": str,
        "chamada_para_acao": str,
        "tipo_de_conteudo": str,
        "conteudos_semanais": list
    }

    for field, expected_type in required_fields.items():
        if field not in brief_data:
            raise ValueError(f"Campo obrigatório '{field}' faltando no briefing do cliente.")
        if not isinstance(brief_data[field], expected_type):
            raise ValueError(f"Campo '{field}' deve ser do tipo {expected_type.__name__}, mas é {type(brief_data[field]).__name__}.")

    # Validação específica para conteudos_semanais
    if "conteudos_semanais" in brief_data:
        if not brief_data["conteudos_semanais"]:
            raise ValueError("A lista 'conteudos_semanais' não pode estar vazia.")
        for i, item in enumerate(brief_data["conteudos_semanais"]):
            if not isinstance(item, dict):
                raise ValueError(f"Item {i} em 'conteudos_semanais' deve ser um dicionário.")
            if "objetivo_do_conteudo_individual" not in item:
                raise ValueError(f"Campo 'objetivo_do_conteudo_individual' faltando no item {i} de 'conteudos_semanais'.")
            if not isinstance(item["objetivo_do_conteudo_individual"], str):
                raise ValueError(f"Campo 'objetivo_do_conteudo_individual' no item {i} de 'conteudos_semanais' deve ser uma string.")

    # 1. Inicializar o Banco de Dados
    print("Inicializando o banco de dados...")
    init_db()
    print("Banco de dados pronto.")

    # Definir e criar diretório de saída para os arquivos gerados
    output_dir = os.path.join(BASE_DIR, "output_files")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Diretório de saída para arquivos gerados: {output_dir}")

    # 2. Coletar Briefing do Cliente a partir de arquivo JSON
    print("\n--- Coleta de Briefing do Cliente (via JSON) ---")
    briefing_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_briefing.json')
    brief_data = load_briefing_from_json(briefing_filepath)

    if not brief_data:
        print("Não foi possível carregar os dados do briefing. Encerrando.")
        return

    try:
        validate_briefing_data(brief_data)
    except ValueError as e:
        print(f"Erro de validação no briefing: {e}")
        return

    nome_do_cliente = brief_data.get("nome_do_cliente", "")
    subnicho = brief_data.get("subnicho", "")
    informacoes_de_contato = brief_data.get("informacoes_de_contato", "")
    publico_alvo = brief_data.get("publico_alvo", "")
    tom_de_voz = brief_data.get("tom_de_voz", "")
    exemplos_de_nicho = brief_data.get("exemplos_de_nicho", [])
    tipo_de_conteudo = brief_data.get("tipo_de_conteudo", "")
    conteudos_semanais = brief_data.get("conteudos_semanais", [])
    objetivos_de_marketing = brief_data.get("objetivos_de_marketing", "")

    if not nome_do_cliente:
        print("Erro: 'nome_do_cliente' não encontrado no arquivo de briefing. Encerrando.")
        return

    print(f"Briefing carregado para o cliente: {nome_do_cliente}")

    # 3. Obter/Criar Perfil do Cliente
    print(f"\nVerificando perfil para '{nome_do_cliente}'...")
    client_profile = get_client_profile(nome_do_cliente)

    if not client_profile:
        print(f"Perfil para '{nome_do_cliente}' não encontrado. Criando novo perfil...")
        insert_client_profile(
            client_name=nome_do_cliente,
            contact_info=informacoes_de_contato,
            public_target=publico_alvo,
            tone_of_voice=tom_de_voz,
            niche_examples=exemplos_de_nicho,
            status='active'
        )
        client_profile = get_client_profile(nome_do_cliente) # Recupera o perfil recém-criado
        print("Novo perfil de cliente criado.")
    else:
        print(f"Perfil para '{nome_do_cliente}' encontrado. Usando perfil existente.")

    # 4. Gerar Conteúdo
    print("\n--- Gerando Conteúdo para Redes Sociais ---")
    try:
        # generate_content_for_client espera dicionários para profile e guidelines
        # Extrair os objetivos individuais dos dicionários em conteudos_semanais
        weekly_themes_list = [item.get("objetivo_do_conteudo_individual", "") for item in conteudos_semanais]

        generated_data = generate_content_for_client(
            client_profile=brief_data, # Usando brief_data como client_profile para este exemplo
            content_type=tipo_de_conteudo,
            weekly_themes=weekly_themes_list,
            weekly_goal=objetivos_de_marketing
        )

        if generated_data.get("status") == "error":
            print(f"Erro ao gerar conteúdo: {generated_data.get("message", "Erro desconhecido")}")
            return

        generated_content = generated_data["generated_content"]
        prompt_used_for_content_generation = generated_data["prompt_sent"]
        tokens_consumed = generated_data["token_usage"]["estimated_input_tokens"]
        api_cost_usd = generated_data["token_usage"]["estimated_cost_usd"]
        print("Conteúdo gerado com sucesso!")

        # Log do prompt utilizado
        log_prompt(nome_do_cliente, prompt_used_for_content_generation, "content_generation")

    except Exception as e:
        print(f"Erro ao gerar conteúdo: {e}")
        return

    # 5. Salvar Briefing e Conteúdo no Banco de Dados
    print("\nSalvando briefing e conteúdo no banco de dados...")
    # Usar um formato de data/hora mais detalhado para evitar sobrescrita
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    delivery_date = datetime.now().strftime('%Y-%m-%d')

    # Adicionar a data de entrega ao conteúdo gerado para uso no HTML
    generated_content["generation_date"] = delivery_date

    insert_brief(
        client_name=nome_do_cliente,
        subniche=subnicho,
        brief_data=brief_data,
        generated_content=generated_content,
        prompt_used=prompt_used_for_content_generation,
        tokens_consumed=tokens_consumed,
        api_cost_usd=api_cost_usd,
        delivery_date=delivery_date
    )
    print(f"Briefing para '{nome_do_cliente}' inserido com sucesso.")
    print("Briefing e conteúdo salvos no DB.")

    # Verificar se os dados foram realmente salvos
    all_briefs = get_all_briefs()
    print("\n--- Verificando dados no banco de dados ---")
    if all_briefs:
        print(f"Total de {len(all_briefs)} briefings encontrados no DB.")
        for brief in all_briefs:
            print(f"  - ID: {brief['id']}, Cliente: {brief['client_name']}, Subnicho: {brief['subniche']}")
    else:
        print("Nenhum briefing encontrado no DB.")
    print("------------------------------------------")

    # 6. Gerar PDF
    print("\n--- Gerando PDF do Briefing ---")
    output_pdf_filename = os.path.join(output_dir, f"briefing_{nome_do_cliente.replace(' ', '_')}_{timestamp}.pdf")
    try:
        create_briefing_pdf(generated_content, nome_do_cliente, output_pdf_filename)
        print(f"PDF do briefing gerado em: {output_pdf_filename}")
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return

    # 7. Gerar HTML
    print("\n--- Gerando Relatório HTML ---")
    output_html_filename = os.path.join(output_dir, f"briefing_{nome_do_cliente.replace(' ', '_')}_{timestamp}.html")
    try:
        create_briefing_html(generated_content, nome_do_cliente, output_html_filename)
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