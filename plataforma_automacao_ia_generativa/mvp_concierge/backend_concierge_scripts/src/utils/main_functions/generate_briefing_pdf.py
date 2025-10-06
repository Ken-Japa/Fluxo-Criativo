import os
from datetime import datetime
from src.pdf_generator import create_briefing_pdf

def generate_briefing_pdf(generated_content, nome_do_cliente, output_dir):
    """
    Gera um arquivo PDF do briefing com o conteúdo gerado.

    Args:
        generated_content (str): O conteúdo gerado para incluir no PDF.
        nome_do_cliente (str): O nome do cliente para nomear o arquivo PDF.
        output_dir (str): O diretório onde o PDF será salvo.

    Returns:
        str: O caminho completo do arquivo PDF gerado, ou None em caso de erro.
    """
    print("\n--- Gerando PDF do Briefing ---")
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_pdf_filename = os.path.join(output_dir, f"briefing_{nome_do_cliente.replace(' ', '_')}_{timestamp}.pdf")
    try:
        create_briefing_pdf(generated_content, nome_do_cliente, output_pdf_filename)
        print(f"PDF do briefing gerado em: {output_pdf_filename}")
        return output_pdf_filename
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None