import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from datetime import datetime

from .config import COMPANY_NAME, LOGO_PATH

def create_briefing_pdf(content_json: dict, client_name: str, output_filename: str):
    """
    Converte o JSON de conteúdo gerado em um "PDF de Briefing Profissional".

    Args:
        content_json (dict): O objeto JSON com os posts, legendas, variações, hashtags e formatos.
        client_name (str): Nome do cliente para personalizar o PDF.
        output_filename (str): Nome do arquivo PDF a ser salvo.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # --- Estilos Personalizados ---
    # Título Principal
    styles.add(ParagraphStyle(name='TitleStyle', 
                               fontSize=24, 
                               leading=28, 
                               alignment=TA_CENTER, 
                               spaceAfter=20,
                               fontName='Helvetica-Bold'))
    # Subtítulo
    styles.add(ParagraphStyle(name='SubtitleStyle', 
                               fontSize=14, 
                               leading=16, 
                               alignment=TA_CENTER, 
                               spaceAfter=10,
                               fontName='Helvetica'))
    # Título da Seção
    styles.add(ParagraphStyle(name='SectionTitle', 
                               fontSize=18, 
                               leading=22, 
                               spaceBefore=20, 
                               spaceAfter=10,
                               fontName='Helvetica-Bold', 
                               textColor=HexColor('#333366')))
    # Título do Post
    styles.add(ParagraphStyle(name='PostTitle', 
                               fontSize=16, 
                               leading=18, 
                               spaceBefore=15, 
                               spaceAfter=5,
                               fontName='Helvetica-Bold'))
    # Texto Normal
    styles.add(ParagraphStyle(name='NormalText', 
                               fontSize=10, 
                               leading=12, 
                               spaceAfter=5,
                               fontName='Helvetica'))
    # Checklist
    styles.add(ParagraphStyle(name='ChecklistItem', 
                               fontSize=10, 
                               leading=14, 
                               spaceBefore=3,
                               fontName='Helvetica'))

    # --- Capa do PDF ---
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph(f"Calendário Semanal de Conteúdo", styles['TitleStyle']))
    story.append(Paragraph(f"para {client_name}", styles['SubtitleStyle']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(COMPANY_NAME, styles['SubtitleStyle']))
    story.append(Spacer(1, 0.5 * inch))
    
    # Inserir Logo
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image(LOGO_PATH)
            # Ajusta o tamanho do logo para caber na página, mantendo a proporção
            logo_width = 1.5 * inch
            logo_height = logo.drawHeight * (logo_width / logo.drawWidth)
            logo.drawWidth = logo_width
            logo.drawHeight = logo_height
            story.append(logo)
            story.append(Spacer(1, 0.2 * inch))
        except Exception as e:
            print(f"Erro ao carregar o logo: {e}")
            story.append(Paragraph("[ERRO AO CARREGAR LOGO]", styles['SubtitleStyle']))
    else:
        story.append(Paragraph("[LOGO NÃO ENCONTRADO]", styles['SubtitleStyle']))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y')}", styles['SubtitleStyle']))
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("---", styles['SubtitleStyle']))
    story.append(Spacer(1, 0.5 * inch))

    # --- Seção de Posts ---
    story.append(Paragraph("Ideias de Conteúdo para a Semana", styles['SectionTitle']))
    story.append(Spacer(1, 0.2 * inch))

    for i, post in enumerate(content_json.get('posts', [])):
        story.append(Paragraph(f"Post {i+1}: {post.get('legenda_principal', 'Título da Ideia do Post')}", styles['PostTitle']))
        
        story.append(Paragraph("Legenda Principal:", styles['NormalText']))
        story.append(Paragraph(post.get('legenda_principal', 'N/A'), styles['NormalText']))
        story.append(Spacer(1, 0.1 * inch))

        if post.get('variacoes_legenda'):
            story.append(Paragraph("Variações de Legenda:", styles['NormalText']))
            for variacao in post['variacoes_legenda']:
                story.append(Paragraph(f"- {variacao}", styles['NormalText']))
            story.append(Spacer(1, 0.1 * inch))

        if post.get('hashtags'):
            story.append(Paragraph("Hashtags:", styles['NormalText']))
            story.append(Paragraph(" ".join(post['hashtags']), styles['NormalText']))
            story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph("Sugestão de Formato:", styles['NormalText']))
        story.append(Paragraph(post.get('formato_sugerido', 'N/A'), styles['NormalText']))
        story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph("Sugestões Visuais:", styles['NormalText']))
        story.append(Paragraph("[ESPAÇO PARA SUGESTÕES VISUAIS - PREENCHER MANUALMENTE OU COM IA FUTURA]", styles['NormalText']))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Checklist de Publicação:", styles['NormalText']))
        story.append(Paragraph("✅ Post Publicado?", styles['ChecklistItem']))
        story.append(Paragraph("✅ Stories Respondidos?", styles['ChecklistItem']))
        story.append(Paragraph("✅ Interação com Comentários?", styles['ChecklistItem']))
        story.append(Spacer(1, 0.4 * inch))

    doc.build(story)