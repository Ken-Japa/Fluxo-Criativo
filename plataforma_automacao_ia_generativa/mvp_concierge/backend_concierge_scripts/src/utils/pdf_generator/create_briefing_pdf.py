import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, PageBreak, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib import colors

from src.utils.pdf_generator._build_cover_page import _build_cover_page
from src.utils.pdf_generator._build_executive_summary import _build_executive_summary
from src.utils.pdf_generator._build_post_section import _build_post_section
from src.utils.pdf_generator._build_publication_calendar import _build_publication_calendar
from src.utils.pdf_generator._build_publication_checklist import _build_publication_checklist
from src.utils.pdf_generator._header_footer import _header_footer
from src.utils.pdf_generator.calendar_logic import generate_publication_calendar
from src.utils.pdf_generator.checklist_logic import generate_publication_checklist

def create_briefing_pdf(content_json: dict, client_name: str, period: str, output_filename: str, target_audience: str = "", tone_of_voice: str = "", marketing_objectives: str = ""):
    """
    Converte o JSON de conteúdo gerado em um "PDF de Briefing Profissional".

    Args:
        content_json (dict): O objeto JSON com os posts, legendas, variações, hashtags e formatos.
        client_name (str): Nome do cliente para personalizar o PDF.
        period (str): O período do briefing (ex: "10/03/2024 - 16/03/2024").
        output_filename (str): Nome do arquivo PDF a ser salvo.
        target_audience (str): O público-alvo do briefing.
        tone_of_voice (str): O tom de voz a ser utilizado no briefing.
        marketing_objectives (str): Os objetivos de marketing do briefing.
    """
    # Salvar o content_json bruto em um arquivo para depuração
    debug_output_dir = r'c:\Users\Ken\Desktop\Prog2\Geracao-Conteudo\plataforma_automacao_ia_generativa\mvp_concierge\backend_concierge_scripts\src\output_files\respostas_IA\\'
    os.makedirs(debug_output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_file_path = os.path.join(debug_output_dir, f"content_json_debug_{timestamp}.json")
    with open(debug_file_path, 'w', encoding='utf-8') as f:
        json.dump(content_json, f, indent=4, ensure_ascii=False)
    print(f"Content_json salvo para depuração em: {debug_file_path}")

    # Garante que content_json é um dicionário, caso seja passado como string JSON
    if isinstance(content_json, str):
        try:
            content_json = json.loads(content_json)
        except json.JSONDecodeError:
            content_json = {}
    elif not isinstance(content_json, dict):
        content_json = {}

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

    # Definir frames para o template de página normal
    frame_width = letter[0] - 2 * inch
    frame_height = letter[1] - 2 * inch
    normal_frame = Frame(inch,
                         inch,
                         frame_width,
                         frame_height,
                         id='normal')

    normal_page_template = PageTemplate(id='NormalPage', frames=normal_frame, onPage=_header_footer)

    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    doc.addPageTemplates([normal_page_template])

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

    # Estilos para o Checklist de Publicação com cores por post e tipo de tarefa
    # Cores base para os posts
    POST_COLORS = {
        1: {"strong": HexColor('#1A237E'), "medium": HexColor('#5C6BC0'), "light": HexColor('#9FA8DA')}, # Azul
        2: {"strong": HexColor('#2E7D32'), "medium": HexColor('#66BB6A'), "light": HexColor('#A5D6A7')}, # Verde
        3: {"strong": HexColor('#EF6C00'), "medium": HexColor('#FFA726'), "light": HexColor('#FFCC80')}, # Laranja
        4: {"strong": HexColor('#4A148C'), "medium": HexColor('#9575CD'), "light": HexColor('#B39DDB')}, # Roxo
        5: {"strong": HexColor('#B71C1C'), "medium": HexColor('#E57373'), "light": HexColor('#EF9A9A')}  # Vermelho
    }

    # Adicionar estilos para cada tipo de tarefa e post
    for i in range(1, 6):
        # Estilo para Postar (cor forte)
        styles.add(ParagraphStyle(name=f'ChecklistPostar_Post{i}',
                                   fontSize=10,
                                   leading=12,
                                   spaceBefore=3,
                                   spaceAfter=3,
                                   fontName='Helvetica-Bold',
                                   textColor=POST_COLORS[i]["strong"]))
        # Estilo para Preparar (cor média)
        styles.add(ParagraphStyle(name=f'ChecklistPreparar_Post{i}',
                                   fontSize=10,
                                   leading=12,
                                   spaceBefore=3,
                                   spaceAfter=3,
                                   fontName='Helvetica',
                                   textColor=POST_COLORS[i]["medium"]))
        # Estilo para Responder (cor clara)
        styles.add(ParagraphStyle(name=f'ChecklistResponder_Post{i}',
                                   fontSize=10,
                                   leading=12,
                                   spaceBefore=3,
                                   spaceAfter=3,
                                   fontName='Helvetica-Oblique',
                                   textColor=POST_COLORS[i]["light"]))



    # Título da Seção
    styles.add(ParagraphStyle(name='SectionTitle',
                               fontSize=22,
                               leading=26,
                               spaceBefore=30,
                               spaceAfter=15,
                               fontName='Helvetica-Bold',
                               textColor=HexColor('#1A237E'), # Azul escuro
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
                           fontSize=18, 
                           leading=22, 
                           fontName='Helvetica-Bold', 
                           alignment=TA_CENTER, # Centralizado
                           spaceAfter=12,
                           textColor=HexColor('#3F51B5'))) # Azul médio para o título do Post
    styles.add(ParagraphStyle(name='PostSubtitle', 
                           fontSize=12, 
                           leading=16, 
                           fontName='Helvetica-Bold', 
                           spaceBefore=10, 
                           spaceAfter=4,
                           textColor=HexColor('#424242'))) # Subtítulo do Post (cor padrão)
    styles.add(ParagraphStyle(name='ColoredPostSubtitle', # Novo estilo para subtítulos coloridos (azul)
                           fontSize=12, 
                           leading=16, 
                           fontName='Helvetica-Bold', 
                           spaceBefore=10, 
                           spaceAfter=4,
                           textColor=HexColor('#3F51B5'))) # Azul médio para subtítulos
    styles.add(ParagraphStyle(name='NeutralPostSubtitle', fontName='Helvetica-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#616161')))
    styles.add(ParagraphStyle(name='BlackSubtitle', fontName='Helvetica-Bold', fontSize=11, leading=12, textColor=colors.black))
    styles.add(ParagraphStyle(name='PurpleSubtitle', fontName='Helvetica-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#800080')))
    styles.add(ParagraphStyle(name='StrongPurpleSubtitle', fontName='Helvetica-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#6A0DAD')))
    styles.add(ParagraphStyle(name='DarkGreenSubtitle', fontName='Helvetica-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#006400')))
    styles.add(ParagraphStyle(name='BrownSubtitle', fontName='Helvetica-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#A52A2A')))
    styles.add(ParagraphStyle(name='PostText', 
                           fontSize=10, 
                           leading=14, 
                           fontName='Helvetica', 
                           spaceAfter=4,
                           textColor=HexColor('#424242'))) # Texto do Post
    styles.add(ParagraphStyle(name='PostContent', # Novo estilo para o conteúdo das subsessões
                           fontSize=10, 
                           leading=14, 
                           fontName='Helvetica', 
                           spaceAfter=4,
                           leftIndent=12, # Recuo para o conteúdo
                           textColor=HexColor('#424242'))) 
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
    # Estilo para datas no checklist
    styles.add(ParagraphStyle(name='ChecklistDate', 
                               fontSize=12, 
                               leading=16, 
                               spaceBefore=10, 
                               fontName='Helvetica-Bold',
                               textColor=HexColor('#000000'))) # Preto
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

    # --- Página de Rosto ---
    story.extend(_build_cover_page(styles, client_name, period))

    # --- Sumário Executivo / Visão Geral da Semana ---
    story.append(PageBreak()) # Adiciona quebra de página antes do sumário executivo
    weekly_strategy_summary_content = content_json.get('weekly_strategy_summary', '')
    if isinstance(weekly_strategy_summary_content, str):
        # Se for uma string, tenta carregar como JSON. Se falhar, usa a string como summary.
        try:
            weekly_strategy_summary_dict = json.loads(weekly_strategy_summary_content)
        except json.JSONDecodeError:
            weekly_strategy_summary_dict = {'summary': weekly_strategy_summary_content}
    elif isinstance(weekly_strategy_summary_content, dict):
        weekly_strategy_summary_dict = weekly_strategy_summary_content
    else:
        weekly_strategy_summary_dict = {}
    story.extend(_build_executive_summary(styles, weekly_strategy_summary_dict, target_audience, tone_of_voice, marketing_objectives))

    # --- Seção de Posts ---
    story.append(PageBreak()) 
    story.append(Paragraph("Ideias de Conteúdo para a Semana", styles['SectionTitle']))
    story.append(Spacer(1, 36)) 

    posts = content_json.get('posts', [])
    if isinstance(posts, str):
        try:
            posts = json.loads(posts)
        except json.JSONDecodeError:
            posts = []
    if not isinstance(posts, list):
        posts = []

    for i, post in enumerate(posts):
        # Garante que cada 'post' individual é um dicionário
        if isinstance(post, str):
            try:
                post = json.loads(post)
            except json.JSONDecodeError:
                post = {}
        elif not isinstance(post, dict):
            post = {}
        story.extend(_build_post_section(styles, post, i + 1))
        if i < len(posts) - 1:
            story.append(PageBreak())

    # --- Calendário de Publicação ---
    # Gerar o calendário de publicação com base na data atual e na lista de posts
    today = datetime.now()
    publication_calendar = generate_publication_calendar(today, posts)
    story.extend(_build_publication_calendar(styles, publication_calendar))

    # --- Checklist de Publicação ---
    # story.append(PageBreak()) # Removido, pois o PageBreak anterior já cuida disso
    story.append(Spacer(1, 36))

    publication_checklist = generate_publication_checklist(publication_calendar)
    story.extend(_build_publication_checklist(styles, publication_checklist))

    doc.build(story)

    return story