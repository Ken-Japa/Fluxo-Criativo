import json
from datetime import datetime
from src.utils.pdf_generator.calendar_logic import generate_publication_calendar
from src.utils.pdf_generator.checklist_logic import generate_publication_checklist

def create_briefing_html(content_json: dict, client_name: str, output_filename: str = "briefing.html", target_audience: str = "", tone_of_voice: str = "", marketing_objectives: str = ""):
    """
    Gera um arquivo HTML de briefing profissional a partir de um JSON de conteúdo.
    O `content_json` deve conter uma lista de posts dentro da chave 'generated_content' -> 'posts'.
    Recomenda-se que o JSON contenha 5 posts para um briefing semanal.

    Args:
        content_json (dict): O JSON contendo os dados do conteúdo gerado.
        client_name (str): O nome do cliente para o qual o briefing está sendo gerado.
        output_filename (str): O nome do arquivo HTML de saída. Padrão é "briefing.html".
        target_audience (str): O público-alvo do briefing.
        tone_of_voice (str): O tom de voz a ser utilizado no briefing.
        marketing_objectives (str): Os objetivos de marketing do briefing.
    """


    # Determine the generation date
    generation_date_str = content_json.get("generation_date")
    if not generation_date_str:
        generation_date_str = content_json.get("generated_content", {}).get("generation_date")
    if not generation_date_str:
        generation_date_str = datetime.now().strftime("%d/%m/%Y")

    # --- Sumário Executivo ---
    weekly_strategy_summary_content = content_json.get('weekly_strategy_summary', '')
    if isinstance(weekly_strategy_summary_content, str):
        try:
            weekly_strategy_summary_dict = json.loads(weekly_strategy_summary_content)
        except json.JSONDecodeError:
            weekly_strategy_summary_dict = {'summary': weekly_strategy_summary_content}
    elif isinstance(weekly_strategy_summary_content, dict):
        weekly_strategy_summary_dict = weekly_strategy_summary_content
    else:
        weekly_strategy_summary_dict = {}

    summary_html = ""
    if weekly_strategy_summary_dict:
        summary_html += "        <h2>Sumário Executivo</h2>\n"
        summary_html += f"        <p>{weekly_strategy_summary_dict.get('summary', 'N/A')}</p>\n"
        if target_audience:
            summary_html += f"        <h3>Público-Alvo:</h3><p>{target_audience}</p>\n"
        if tone_of_voice:
            summary_html += f"        <h3>Tom de Voz:</h3><p>{tone_of_voice}</p>\n"
        if marketing_objectives:
            summary_html += f"        <h3>Objetivos de Marketing:</h3><p>{marketing_objectives}</p>\n"

    # --- Calendário de Publicação ---
    today = datetime.now()
    posts = content_json.get('posts', [])
    publication_calendar = generate_publication_calendar(today, posts)

    calendar_html = ""
    if publication_calendar:
        calendar_html += "        <h2>Calendário de Publicação</h2>\n"
        calendar_html += "        <table class=\"calendar-table\">\n"
        calendar_html += "            <thead>\n"
        calendar_html += "                <tr><th>Dia</th><th>Data</th><th>Post</th></tr>\n"
        calendar_html += "            </thead>\n"
        calendar_html += "            <tbody>\n        """
        for entry in publication_calendar:
            for sub_entry in entry['entries']:
                calendar_html += f"                <tr><td>{entry['day'].split(', ')[0]}</td><td>{entry['day'].split(', ')[1]}</td><td>{sub_entry['content']}</td></tr>\n"
        calendar_html += "            </tbody>\n"
        calendar_html += "        </table>\n"

    # --- Checklist de Publicação ---
    publication_checklist = generate_publication_checklist(publication_calendar)
    checklist_html = ""
    if publication_checklist:
        checklist_html += "        <h2>Checklist de Publicação</h2>\n"
        checklist_html += "        <ul class=\"checklist\">\n"
        for item in publication_checklist:
            checklist_html += f"            <li>{item}</li>\n"
        checklist_html += "        </ul>\n"


    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Briefing Profissional - {client_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
        .container {{ width: 80%; margin: 20px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .cover {{ text-align: center; padding: 50px 0; background-color: #0056b3; color: #fff; border-radius: 8px 8px 0 0; margin-bottom: 30px; }}
        .cover h1 {{ margin: 0; font-size: 2.5em; }}
        .cover p {{ font-size: 1.2em; margin-top: 10px; }}
        h2 {{ color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-top: 40px; }}
        h3 {{ color: #0056b3; margin-top: 30px; }}
        .post-section {{ background-color: #e9f5ff; border-left: 5px solid #0056b3; padding: 20px; margin-bottom: 20px; border-radius: 5px; }}
        .post-section p {{ margin: 5px 0; }}
        .checklist {{ list-style-type: none; padding: 0; }}
        .checklist li {{ background: #f0f0f0; margin-bottom: 5px; padding: 10px; border-radius: 3px; }}
        .checklist li:before {{ content: "☐ "; color: #0056b3; font-weight: bold; }} /* Adiciona um quadrado antes do item */
        .calendar-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .calendar-table th, .calendar-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .calendar-table th {{ background-color: #f2f2f2; }}
        .footer {{ text-align: center; margin-top: 50px; font-size: 0.9em; color: #777; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="cover">
            <h1>Briefing de Conteúdo Profissional</h1>
            <p>Para: {client_name}</p>
            <p>Data: {generation_date_str}</p>
        </div>

        <h2>Visão Geral do Conteúdo</h2>
        <p>Este documento apresenta o conteúdo sugerido para as redes sociais do cliente, com base nas diretrizes fornecidas e no perfil do público-alvo.</p>

        {summary_html}
        {calendar_html}
        {checklist_html}

        <h2>Posts Sugeridos</h2>
        """

    # Adiciona os posts dinamicamente
    for i, post in enumerate(content_json.get("posts", [])):
        html_content += f"""
            <div class="post-section">
                <h3>Post #{i + 1}: {post.get("titulo", "Sem Título")}</h3>
                <p><strong>Legenda:</strong> {post.get("legenda_principal", "N/A")}</p>
                <p><strong>Variações:</strong></p>
                <ul>
        """
        for variation in post.get("variacoes_legenda", []):
            html_content += f"                <li>{variation}</li>\n"
        html_content += f"""
                </ul>
                <p><strong>Hashtags:</strong> {" ".join(post.get("hashtags", []))}</p>
                <p><strong>Formato Sugerido:</strong> {post.get("formato_sugerido", "N/A")}</p>
                <p><strong>Sugestões Visuais:</strong> [ESPAÇO PARA SUGESTÕES VISUAIS - PREENCHER MANUALMENTE OU COM IA FUTURA]</p>
                <p><strong>Checklist de Publicação:</strong></p>
                <ul class="checklist">
                    <li>Revisar texto e gramática.</li>
                    <li>Verificar a qualidade da imagem/vídeo.</li>
                    <li>Confirmar o agendamento.</li>
                    <li>Responder a comentários e mensagens.</li>
                </ul>
            </div>
        """

    # Adiciona o rodapé e fechamento do HTML
    html_content += """
            <div class="footer">
                <p>&copy; 2025 Conteúdo gerado por Fluxo Criativo. Todos os direitos reservados.</p>
            </div>
        </div>
    </body>
</html>
    """

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)