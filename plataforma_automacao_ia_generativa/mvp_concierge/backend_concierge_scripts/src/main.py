import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv

from src.data_storage import init_db, insert_brief, get_client_profile, get_all_briefs, insert_client_profile
from src.content_generator import generate_content_for_client
from src.utils.pdf_generator.create_briefing_pdf import create_briefing_pdf
from src.html_generator import create_briefing_html
from src.utils.briefing_loader import load_briefing_from_json
from src.utils.prompt_logger import log_prompt
from src.config import COMPANY_NAME, BASE_DIR
from src.utils.main_functions.initialize_environment import initialize_environment
from src.utils.main_functions.collect_and_validate_briefing import collect_and_validate_briefing
from src.utils.main_functions.get_or_create_client_profile import get_or_create_client_profile
from src.utils.main_functions.generate_social_media_content import generate_social_media_content
from src.utils.main_functions.save_content_to_database import save_content_to_database
from src.utils.main_functions.generate_briefing_pdf import generate_briefing_pdf
from src.utils.main_functions.generate_briefing_html import generate_briefing_html
from src.utils.main_functions.display_success_message import display_success_message

def main():
    """
    Função principal que orquestra o fluxo de processamento do Concierge MVP.
    Inclui inicialização do DB, coleta de briefing, geração de conteúdo,
    salvamento no DB e geração de PDF.
    """
    print("\n--- Iniciando Concierge MVP ---")

    output_dir = initialize_environment()
    if output_dir is None:
        print("Erro: Falha ao inicializar o ambiente. Encerrando.")
        return

    brief_data, nome_do_cliente, subnicho, informacoes_de_contato, \
    publico_alvo, tom_de_voz, exemplos_de_nicho, tipo_de_conteudo, \
    conteudos_semanais, objetivos_de_marketing = collect_and_validate_briefing()

    if nome_do_cliente is None:
        return

    client_profile = get_or_create_client_profile(
        nome_do_cliente,
        informacoes_de_contato,
        publico_alvo,
        tom_de_voz,
        exemplos_de_nicho
    )

    deepseek_json_output_dir = os.path.join(BASE_DIR, "src", "output_files", "respostas_IA", "Deepseek")
    os.makedirs(deepseek_json_output_dir, exist_ok=True)

    gemini_generated_content, deepseek_generated_content, prompt_used_for_content_generation, tokens_consumed_gemini, api_cost_usd_gemini, tokens_consumed_deepseek, api_cost_usd_deepseek = \
        generate_social_media_content(brief_data, nome_do_cliente, tipo_de_conteudo, conteudos_semanais, objetivos_de_marketing, deepseek_json_output_dir)

    if deepseek_generated_content is None:
        return

    # Remover os caracteres extras e fazer o parse da string JSON
    try:
        # Remove the markdown code block delimiters if they exist
        deepseek_generated_content = deepseek_generated_content.replace("```json", "").replace("```", "")
        # Tenta extrair o objeto JSON usando regex
        json_match = re.search(r'\{.*\}', deepseek_generated_content, re.DOTALL)
        if json_match:
            deepseek_generated_content = json_match.group(0)
        else:
            print("AVISO: Não foi possível extrair o objeto JSON usando regex. Tentando decodificar o conteúdo bruto.")
        # Escapando barras invertidas inválidas na string JSON do DeepSeek para resolver o erro 'Invalid \escape'.
        deepseek_generated_content = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', deepseek_generated_content)
        
        # Salvar o conteúdo formatado do DeepSeek no diretório de respostas da IA
        sanitized_client_name = nome_do_cliente.replace(" ", "_").replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deepseek_formatted_output_path = os.path.join(deepseek_json_output_dir, f"Deepseek_formated-{sanitized_client_name}_{timestamp}.json")
        with open(deepseek_formatted_output_path, "w", encoding="utf-8") as f:
            f.write(deepseek_generated_content)
        print(f"Conteúdo formatado do DeepSeek salvo em: {deepseek_formatted_output_path}")
        
        # Remover vírgulas extras antes de fechar colchetes ou chaves
        deepseek_generated_content = re.sub(r',(\s*[}\]])', r'\1', deepseek_generated_content)
        
        deepseek_generated_content = json.loads(deepseek_generated_content)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar o JSON do DeepSeek: {e}")
        print(f"Conteúdo problemático: {deepseek_generated_content[:500]}...") # Imprime os primeiros 500 caracteres
        return
    except AttributeError as e:
        print(f"Erro de atributo ao processar o conteúdo do DeepSeek: {e}")
        print(f"Tipo de conteúdo: {type(deepseek_generated_content)}")
        return

    # TODO: Desenvolver lógica para enviar os dois JSONs (Gemini e DeepSeek) para o Mistral.
    # Por enquanto, vamos usar o conteúdo do Gemini para as próximas etapas.

    if gemini_generated_content is None:
        return

    # Remover os caracteres extras e fazer o parse da string JSON do Gemini
    try:
        # Remove the markdown code block delimiters if they exist
        gemini_generated_content = gemini_generated_content.replace("```json", "").replace("```", "")
        # Tenta extrair o objeto JSON usando regex
        json_match = re.search(r'\{.*\}', gemini_generated_content, re.DOTALL)
        if json_match:
            gemini_generated_content = json_match.group(0)
        else:
            print("AVISO: Não foi possível extrair o objeto JSON do Gemini usando regex. Tentando decodificar o conteúdo bruto.")
        # Escapando barras invertidas inválidas na string JSON do Gemini para resolver o erro 'Invalid \escape'.
        gemini_generated_content = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', gemini_generated_content)
        
        # Salvar o conteúdo formatado do Gemini no diretório de respostas da IA
        gemini_json_output_dir = os.path.join(BASE_DIR, "src", "output_files", "respostas_IA", "Gemini")
        os.makedirs(gemini_json_output_dir, exist_ok=True)
        sanitized_client_name = nome_do_cliente.replace(" ", "_").replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        gemini_formatted_output_path = os.path.join(gemini_json_output_dir, f"Gemini_formated-{sanitized_client_name}_{timestamp}.json")
        with open(gemini_formatted_output_path, "w", encoding="utf-8") as f:
            f.write(gemini_generated_content)
        print(f"Conteúdo formatado do Gemini salvo em: {gemini_formatted_output_path}")

        # Remover vírgulas extras antes de fechar colchetes ou chaves
        gemini_generated_content = re.sub(r',(\s*[}\]])', r'\1', gemini_generated_content)
        
        gemini_generated_content = json.loads(gemini_generated_content)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar o JSON do Gemini: {e}")
        print(f"Conteúdo problemático: {gemini_generated_content[:500]}...") # Imprime os primeiros 500 caracteres
        return
    except AttributeError as e:
        print(f"Erro de atributo ao processar o conteúdo do Gemini: {e}")
        print(f"Tipo de conteúdo: {type(gemini_generated_content)}")
        return

    save_content_to_database(brief_data, nome_do_cliente, deepseek_generated_content, prompt_used_for_content_generation, tokens_consumed_deepseek, api_cost_usd_deepseek)

    print(f"DEBUG: output_dir before PDF generation: {output_dir}")
    # 6. Gerar PDF Deepseek
    output_pdf_filename_deepseek = generate_briefing_pdf(deepseek_generated_content, nome_do_cliente, output_dir, publico_alvo, tom_de_voz, objetivos_de_marketing, ai_prefix="Deepseek-")
    if output_pdf_filename_deepseek is None:
        return

    # 7. Gerar HTML Deepseek
    output_html_filename_deepseek = generate_briefing_html(deepseek_generated_content, nome_do_cliente, output_dir, ai_prefix="Deepseek-")
    if output_html_filename_deepseek is None:
        return

    # 8. Gerar PDF Gemini
    output_pdf_filename_gemini = generate_briefing_pdf(gemini_generated_content, nome_do_cliente, output_dir, publico_alvo, tom_de_voz, objetivos_de_marketing, ai_prefix="Gemini-")
    if output_pdf_filename_gemini is None:
        return

    # 9. Gerar HTML Gemini
    output_html_filename_gemini = generate_briefing_html(gemini_generated_content, nome_do_cliente, output_dir, ai_prefix="Gemini-")
    if output_html_filename_gemini is None:
        return

    display_success_message(output_pdf_filename_deepseek, api_cost_usd_deepseek)

if __name__ == "__main__":
    main()