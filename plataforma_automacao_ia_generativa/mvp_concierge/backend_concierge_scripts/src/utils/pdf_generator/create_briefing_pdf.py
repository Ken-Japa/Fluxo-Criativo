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

from ..config import COMPANY_NAME, LOGO_PATH
from ._header_footer import _header_footer
from ._build_cover_page import _build_cover_page
from ._build_executive_summary import _build_executive_summary
from ._build_post_section import _build_post_section
from ._build_publication_calendar import _build_publication_calendar
from ._build_publication_checklist import _build_publication_checklist

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