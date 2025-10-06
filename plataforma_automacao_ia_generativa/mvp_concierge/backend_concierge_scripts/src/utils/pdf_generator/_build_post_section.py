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
    post_story.append(Paragraph(f"Post {post_number}: {post.get('title', 'N/A')}", styles['PostTitle']))
    post_story.append(Spacer(1, 0.1 * inch))

    post_story.append(Paragraph("Justificativa Estratégica:", styles['PostSubtitle']))
    post_story.append(Paragraph(post.get('strategic_justification', 'N/A'), styles['PostText']))
    post_story.append(Spacer(1, 0.1 * inch))

    post_story.append(Paragraph("Legenda Principal:", styles['PostSubtitle']))
    post_story.append(Paragraph(post.get('main_caption', 'N/A'), styles['PostText']))
    post_story.append(Spacer(1, 0.1 * inch))

    post_story.append(Paragraph("Variações de Legenda:", styles['PostSubtitle']))
    for variation in post.get('caption_variations', []):
        post_story.append(Paragraph(f"- {variation}", styles['PostText']))
    post_story.append(Spacer(1, 0.1 * inch))

    post_story.append(Paragraph("Hashtags:", styles['PostSubtitle']))
    post_story.append(Paragraph(" ".join(post.get('hashtags', [])), styles['PostHashtag']))
    post_story.append(Spacer(1, 0.1 * inch))

    post_story.append(Paragraph("Sugestão de Formato:", styles['PostSubtitle']))
    post_story.append(Paragraph(post.get('format_suggestion', 'N/A'), styles['PostFormat']))
    post_story.append(Spacer(1, 0.1 * inch))

    post_story.append(Paragraph("Sugestões Visuais Detalhadas:", styles['PostSubtitle']))
    post_story.append(Paragraph(post.get('visual_suggestions', 'N/A'), styles['PostVisuals']))
    post_story.append(Spacer(1, 0.2 * inch))

    return post_story