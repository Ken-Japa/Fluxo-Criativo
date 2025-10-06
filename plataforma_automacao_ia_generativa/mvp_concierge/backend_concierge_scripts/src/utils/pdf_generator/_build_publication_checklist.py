from reportlab.platypus import Paragraph, Spacer, NextPageTemplate, PageBreak

def _build_publication_checklist(styles: dict, publication_checklist: list) -> list:
    """
    Constrói a seção de checklist de publicação do PDF.

    Args:
        styles (dict): Objeto de estilos do ReportLab.
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