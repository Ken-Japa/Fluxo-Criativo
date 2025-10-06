import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, NextPageTemplate, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from datetime import datetime

from .config import COMPANY_NAME, LOGO_PATH

def create_briefing_pdf(content_json: dict, client_name: str, period: str, output_filename: str):
    """
    Converte o JSON de conteúdo gerado em um "PDF de Briefing Profissional".

    Args:
        content_json (dict): O objeto JSON com os posts, legendas, variações, hashtags e formatos.
        client_name (str): Nome do cliente para personalizar o PDF.
        period (str): O período do briefing (ex: "10/03/2024 - 16/03/2024").
        output_filename (str): Nome do arquivo PDF a ser salvo.
    """
    styles = getSampleStyleSheet()
    story = []

    # --- Estilos Personalizados ---
    # Título Principal
    styles.add(ParagraphStyle(name='FooterStyle', 
                               fontSize=9, 
                               leading=10, 
                               alignment=TA_CENTER, 
                               fontName='Helvetica',
                               textColor=HexColor('#757575'))) # Cinza médio

    def _header_footer(canvas, doc):
        canvas.saveState()
        # Footer
        footer_text = f"{COMPANY_NAME} | Página {doc.page}"
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(HexColor('#757575'))
        canvas.drawCentredString(letter[0] / 2.0, 0.75 * inch, footer_text)
        canvas.restoreState()

    doc = SimpleDocTemplate(output_filename, pagesize=letter)

    # Título Principal
    styles.add(ParagraphStyle(name='TitleStyle', 
                               fontSize=32, 
                               leading=38, 
                               alignment=TA_CENTER, 
                               spaceAfter=30,
                               fontName='Helvetica-Bold',
                               textColor=HexColor('#1A237E'))) # Azul escuro
    # Subtítulo
    styles.add(ParagraphStyle(name='SubtitleStyle', 
                               fontSize=18, 
                               leading=22, 
                               alignment=TA_CENTER, 
                               spaceAfter=20,
                               fontName='Helvetica',
                               textColor=HexColor('#3F51B5'))) # Azul médio
    # Título da Seção
    styles.add(ParagraphStyle(name='SectionTitle', 
                               fontSize=22, 
                               leading=26, 
                               spaceBefore=30, 
                               spaceAfter=15,
                               fontName='Helvetica-Bold', 
                               textColor=HexColor('#333366'), # Azul escuro
                               alignment=TA_CENTER,
                               borderPadding=6,
                               backColor=HexColor('#E8EAF6'), # Fundo azul claro
                               borderRadius=5))
    # Texto Normal
styles.add(ParagraphStyle(name='NormalText', 
                           fontSize=11, 
                           leading=14, 
                           spaceAfter=6,
                           fontName='Helvetica',
                           textColor=HexColor('#212121'))) # Quase preto

# Hashtags
styles.add(ParagraphStyle(name='HashtagStyle', 
                           fontSize=11, 
                           leading=14, 
                           spaceAfter=6,
                           fontName='Helvetica-Bold',
                           textColor=HexColor('#3F51B5'))) # Azul médio
styles.add(ParagraphStyle(name='SummaryTitle', 
                           fontSize=16, 
                           leading=20, 
                           fontName='Helvetica-Bold', 
                           alignment=TA_LEFT, 
                           spaceAfter=10,
                           textColor=HexColor('#212121'))) # Título do Sumário
styles.add(ParagraphStyle(name='SummaryText', 
                           fontSize=10, 
                           leading=14, 
                           fontName='Helvetica', 
                           spaceAfter=6,
                           textColor=HexColor('#424242'))) # Texto do Sumário
styles.add(ParagraphStyle(name='PostTitle', 
                           fontSize=14, 
                           leading=18, 
                           fontName='Helvetica-Bold', 
                           spaceAfter=8,
                           textColor=HexColor('#212121'))) # Título do Post
styles.add(ParagraphStyle(name='PostSubtitle', 
                           fontSize=12, 
                           leading=16, 
                           fontName='Helvetica-Bold', 
                           spaceAfter=6,
                           textColor=HexColor('#424242'))) # Subtítulo do Post
styles.add(ParagraphStyle(name='PostText', 
                           fontSize=10, 
                           leading=14, 
                           fontName='Helvetica', 
                           spaceAfter=4,
                           textColor=HexColor('#424242'))) # Texto do Post
styles.add(ParagraphStyle(name='PostHashtag', 
                           fontSize=10, 
                           leading=14, 
                           fontName='Helvetica-Bold',
                           textColor=HexColor('#3F51B5'))) # Hashtag do Post
styles.add(ParagraphStyle(name='PostFormat', 
                           fontSize=10, 
                           leading=14, 
                           fontName='Helvetica-Oblique', 
                           spaceAfter=4,
                           textColor=HexColor('#616161'))) # Formato do Post
styles.add(ParagraphStyle(name='PostVisuals', 
                           fontSize=10, 
                           leading=14, 
                           fontName='Helvetica', 
                           spaceAfter=12,
                           textColor=HexColor('#424242'))) # Sugestões Visuais do Post
styles.add(ParagraphStyle(name='ChecklistTitle', 
                               fontSize=16, 
                               leading=20, 
                               fontName='Helvetica-Bold', 
                               spaceAfter=10,
                               textColor=HexColor('#212121'))) # Título do Checklist
styles.add(ParagraphStyle(name='ChecklistItem', 
                               fontSize=11, 
                               leading=16, 
                               spaceBefore=4,
                               fontName='Helvetica',
                               textColor=HexColor('#212121'))) # Item do Checklist
styles.add(ParagraphStyle(name='CalendarTitle', 
                               fontSize=16, 
                               leading=20, 
                               fontName='Helvetica-Bold', 
                               spaceAfter=10,
                               textColor=HexColor('#212121'))) # Título do Calendário
styles.add(ParagraphStyle(name='CalendarHeader', 
                               fontSize=12, 
                               leading=16, 
                               fontName='Helvetica-Bold', 
                               spaceAfter=6,
                               textColor=HexColor('#424242'))) # Cabeçalho do Calendário
styles.add(ParagraphStyle(name='CalendarEntry', 
                               fontSize=10, 
                               leading=14, 
                               fontName='Helvetica', 
                               spaceAfter=4,
                               textColor=HexColor('#424242'))) # Entrada do Calendário

    # --- Capa do PDF ---
story.extend(_build_cover_page(styles, client_name, period))

    # --- Sumário Executivo / Visão Geral da Semana ---
story.extend(_build_executive_summary(styles, content_json.get('weekly_strategy_summary', {})))

    # --- Seção de Posts ---
story.append(Paragraph("Ideias de Conteúdo para a Semana", styles['SectionTitle']))
story.append(Spacer(1, 0.5 * inch))

for i, post in enumerate(content_json.get('posts', [])):
        story.extend(_build_post_section(styles, post, i + 1))

    # --- Calendário de Publicação Sugerido ---
story.extend(_build_publication_calendar(styles, content_json.get('publication_calendar', [])))

    # --- Checklist de Publicação ---
story.extend(_build_publication_checklist(styles, content_json.get('publication_checklist', [])))

doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)

def _build_cover_page(styles, client_name: str, period: str) -> list:
    cover_story = []
    cover_story.append(Spacer(1, 2.5 * inch))
    cover_story.append(Paragraph(f"Calendário Semanal de Conteúdo", styles['TitleStyle']))
    cover_story.append(Spacer(1, 0.2 * inch))
    cover_story.append(Paragraph(f"para {client_name}", styles['SubtitleStyle']))
    cover_story.append(Spacer(1, 0.5 * inch))
    cover_story.append(Paragraph(f"Período: {period}", styles['SubtitleStyle']))
    cover_story.append(Spacer(1, 0.5 * inch))
    cover_story.append(Paragraph(COMPANY_NAME, styles['SubtitleStyle']))
    cover_story.append(Spacer(1, 0.8 * inch))
    
    # Inserir Logo
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image(LOGO_PATH)
            # Ajusta o tamanho do logo para caber na página, mantendo a proporção
            logo_width = 2.5 * inch  # Aumenta o tamanho do logo
            logo_height = logo.drawHeight * (logo_width / logo.drawWidth)
            logo.drawWidth = logo_width
            logo.drawHeight = logo_height
            logo.hAlign = 'CENTER'
            cover_story.append(logo)
            cover_story.append(Spacer(1, 0.5 * inch))
        except Exception as e:
            print(f"Erro ao carregar o logo: {e}")
            cover_story.append(Paragraph("[ERRO AO CARREGAR LOGO]", styles['SubtitleStyle']))
    else:
        cover_story.append(Paragraph("[LOGO NÃO ENCONTRADO]", styles['SubtitleStyle']))
    cover_story.append(Spacer(1, 0.5 * inch))

    cover_story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y')}", styles['SubtitleStyle']))
    cover_story.append(Spacer(1, 1.5 * inch))
    cover_story.append(HRFlowable(width="100%", thickness=1.5, lineCap='round', color=HexColor('#000000'), spaceBefore=1, spaceAfter=1, hAlign='CENTER')) # Adiciona uma linha separadora
    cover_story.append(Spacer(1, 0.7 * inch))
    return cover_story

def _build_executive_summary(styles, weekly_strategy_summary: dict) -> list:
    summary_story = []
    summary_story.append(NextPageTemplate('NormalPage'))
    summary_story.append(PageBreak())
    summary_story.append(Paragraph("Sumário Executivo", styles['SectionTitle']))
    summary_story.append(Spacer(1, 0.3 * inch))

    summary_story.append(Paragraph("Resumo da Estratégia Semanal:", styles['SummaryTitle']))
    summary_story.append(Paragraph(weekly_strategy_summary.get('summary', 'N/A'), styles['SummaryText']))
    summary_story.append(Spacer(1, 0.2 * inch))

    summary_story.append(Paragraph("Objetivos:", styles['SummaryTitle']))
    for objective in weekly_strategy_summary.get('objectives', []):
        summary_story.append(Paragraph(f"- {objective}", styles['SummaryText']))
    summary_story.append(Spacer(1, 0.2 * inch))

    summary_story.append(Paragraph("Público-Alvo:", styles['SummaryTitle']))
    summary_story.append(Paragraph(weekly_strategy_summary.get('target_audience', 'N/A'), styles['SummaryText']))
    summary.story.append(Spacer(1, 0.2 * inch))

    summary_story.append(Paragraph("Tom de Voz:", styles['SummaryTitle']))
    summary_story.append(Paragraph(weekly_strategy_summary.get('tone_of_voice', 'N/A'), styles['SummaryText']))
    summary_story.append(Spacer(1, 0.5 * inch))

    return summary_story

def _build_post_section(styles, post: dict, post_number: int) -> list:
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

def _build_publication_calendar(styles, publication_calendar: list) -> list:
    calendar_story = []
    calendar_story.append(NextPageTemplate('NormalPage'))
    calendar_story.append(PageBreak())
    calendar_story.append(Paragraph("Calendário de Publicação Sugerido", styles['SectionTitle']))
    calendar_story.append(Spacer(1, 0.3 * inch))

    if not publication_calendar:
        calendar_story.append(Paragraph("Nenhum calendário de publicação sugerido disponível.", styles['NormalText']))
        return calendar_story

def _build_publication_checklist(styles, publication_checklist: list) -> list:
    """
    Constrói a seção de checklist de publicação do PDF.

    Args:
        styles: Objeto de estilos do ReportLab.
        publication_checklist (list): Lista de itens do checklist de publicação.

    Returns:
        list: Uma lista de elementos Story para o checklist de publicação.
    """
    checklist_story = []
    checklist_story.append(NextPageTemplate('NormalPage'))
    checklist_story.append(PageBreak())
    checklist_story.append(Paragraph("Checklist de Publicação", styles['SectionTitle']))
    checklist_story.append(Spacer(1, 0.3 * inch))

    if not publication_checklist:
        checklist_story.append(Paragraph("Nenhum checklist de publicação disponível.", styles['NormalText']))
        return checklist_story

    for item in publication_checklist:
        checklist_story.append(Paragraph(f"- {item}", styles['ChecklistItem']))
        checklist_story.append(Spacer(1, 0.1 * inch))

    return checklist_story

    for day_entry in publication_calendar:
        calendar_story.append(Paragraph(day_entry.get('day', 'N/A'), styles['CalendarTitle']))
        for entry in day_entry.get('entries', []):
            calendar_story.append(Paragraph(f"- {entry.get('time', 'N/A')} - {entry.get('content', 'N/A')}", styles['CalendarEntry']))
        calendar_story.append(Spacer(1, 0.2 * inch))

    return calendar_story