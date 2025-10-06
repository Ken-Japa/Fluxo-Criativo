from reportlab.platypus import Paragraph, Spacer

def _build_post_section(styles: dict, post: dict, post_number: int) -> list:
    """
    Constrói a seção de um post individual no PDF.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        post (dict): Dicionário com os dados de um post.
        post_number (int): Número do post.

    Returns:
        list: Uma lista de elementos Story para a seção do post.
    """
    post_story = []
    post_story.append(Paragraph(f"Post {post_number}: {post.get('titulo', 'N/A')}", styles['PostTitle']))
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Justificativa Estratégica:", styles['BlackSubtitle']))
    post_story.append(Paragraph(post.get('post_strategy_rationale', 'N/A'), styles['PostContent']))
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Legenda Principal:", styles['PurpleSubtitle']))
    post_story.append(Paragraph(post.get('legenda_principal', 'N/A'), styles['PostContent']))
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Variações de Legenda:", styles['StrongPurpleSubtitle']))
    for i, variation in enumerate(post.get('variacoes_legenda', [])):
        post_story.append(Paragraph(f"{i+1}. {variation}", styles['PostContent']))
        if i < len(post.get('variacoes_legenda', [])) - 1:
            post_story.append(Spacer(1, 3.6)) # Espaço menor entre as variações
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Hashtags:", styles['BlackSubtitle']))
    post_story.append(Paragraph(" ".join(post.get('hashtags', [])), styles['PostHashtag']))
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Sugestão de Formato:", styles['DarkGreenSubtitle']))
    post_story.append(Paragraph(post.get('sugestao_formato', 'N/A'), styles['PostContent']))
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Sugestões Visuais Detalhadas:", styles['BrownSubtitle']))
    post_story.append(Paragraph(post.get('visual_prompt_suggestion', 'N/A'), styles['PostContent']))
    post_story.append(Spacer(1, 14.4))

    return post_story