import json
import os
from datetime import datetime

from src.utils.pdf_generator.create_briefing_pdf import create_briefing_pdf

def generate_briefing_pdf(content_json: dict, client_name: str, output_filename: str):
    """
    Gera um briefing em PDF com base no conteúdo JSON fornecido.

    Args:
        content_json (dict): O conteúdo JSON gerado pela IA.
        client_name (str): O nome do cliente.
        output_filename (str): O nome do arquivo de saída do PDF.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Caminho para o client_briefing.json
    briefing_path = os.path.join(os.path.dirname(__file__), "..", "client_briefing.json")
    
    target_audience = "N/A"
    tone_of_voice = "N/A"
    marketing_objectives = "N/A"

    if os.path.exists(briefing_path):
        with open(briefing_path, 'r', encoding='utf-8') as f:
            briefing_data = json.load(f)
            target_audience = briefing_data.get("publico_alvo", "N/A")
            tone_of_voice = briefing_data.get("tom_de_voz", "N/A")
            marketing_objectives = briefing_data.get("objetivos_de_marketing", "N/A")

    create_briefing_pdf(
        content_json=content_json,
        client_name=client_name,
        period=timestamp,
        output_filename=output_filename,
        target_audience=target_audience,
        tone_of_voice=tone_of_voice,
        marketing_objectives=marketing_objectives
    )