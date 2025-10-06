from reportlab.platypus import Paragraph, Spacer, NextPageTemplate, PageBreak

def _build_publication_calendar(styles: dict, publication_calendar: list) -> list:
    """
    Constrói a seção de calendário de publicação do PDF.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        publication_calendar (list): Lista de entradas do calendário de publicação.

    Returns:
        list: Uma lista de elementos Story para o calendário de publicação.
    """
    calendar_story = []
    calendar_story.append(NextPageTemplate('NormalPage'))
    calendar_story.append(PageBreak())
    calendar_story.append(Paragraph("Calendário de Publicação Sugerido", styles['SectionTitle']))
    calendar_story.append(Spacer(1, 0.3 * inch))

    if not publication_calendar:
        calendar_story.append(Paragraph("Nenhum calendário de publicação sugerido disponível.", styles['NormalText']))
        return calendar_story

    for day_entry in publication_calendar:
        calendar_story.append(Paragraph(day_entry.get('day', 'N/A'), styles['CalendarTitle']))
        for entry in day_entry.get('entries', []):
            calendar_story.append(Paragraph(f"- {entry.get('time', 'N/A')} - {entry.get('content', 'N/A')}", styles['CalendarEntry']))
        calendar_story.append(Spacer(1, 0.2 * inch))

    return calendar_story