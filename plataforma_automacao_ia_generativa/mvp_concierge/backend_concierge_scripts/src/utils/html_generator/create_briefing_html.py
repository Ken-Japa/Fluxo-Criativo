import json
from datetime import datetime

def create_briefing_html(content_json: dict, client_name: str, output_filename: str = "briefing.html"):
    """
    Gera um arquivo HTML de briefing profissional a partir de um JSON de conteúdo.
    O `content_json` deve conter uma lista de posts dentro da chave 'generated_content' -> 'posts'.
    Recomenda-se que o JSON contenha 5 posts para um briefing semanal.

    Args:
        content_json (dict): O JSON contendo os dados do conteúdo gerado.
        client_name (str): O nome do cliente para o qual o briefing está sendo gerado.
        output_filename (str): O nome do arquivo HTML de saída. Padrão é "briefing.html".
    """
    # Determine the generation date
    generation_date_str = content_json.get("generation_date")
    if not generation_date_str:
        generation_date_str = content_json.get("generated_content", {}).get("generation_date")
    if not generation_date_str:
        generation_date_str = datetime.now().strftime("%d/%m/%Y")

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

        <h2>Posts Sugeridos</h2>
    """

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
    print(f"Briefing HTML gerado com sucesso: {output_filename}")