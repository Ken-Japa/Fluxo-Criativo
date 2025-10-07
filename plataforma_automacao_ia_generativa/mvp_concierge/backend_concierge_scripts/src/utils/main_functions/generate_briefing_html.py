import os
from datetime import datetime
from src.html_generator import create_briefing_html

def generate_briefing_html(generated_content, nome_do_cliente, output_dir):
    """
    Gera um arquivo HTML do briefing com o conteúdo gerado.

    Args:
        generated_content (str): O conteúdo gerado para incluir no HTML.
        nome_do_cliente (str): O nome do cliente para nomear o arquivo HTML.
        output_dir (str): O diretório onde o HTML será salvo.

    Returns:
        str: O caminho completo do arquivo HTML gerado, ou None em caso de erro.
    """
    print("\n--- Gerando Relatório HTML ---")
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_html_filename = os.path.join(output_dir, f"briefing_{nome_do_cliente.replace(' ', '_')}_{timestamp}.html")
    try:
        create_briefing_html(generated_content, nome_do_cliente, output_html_filename)
        return output_html_filename
    except Exception as e:
        print(f"Erro ao gerar HTML: {e}")
        return None