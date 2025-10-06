from reportlab.platypus import Paragraph, Spacer, NextPageTemplate, PageBreak

def _build_executive_summary(styles: dict, weekly_strategy_summary: dict) -> list:
    """
    Constrói a seção de sumário executivo do PDF.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        weekly_strategy_summary (dict): Dicionário com o resumo da estratégia semanal.

    Returns:
        list: Uma lista de elementos Story para o sumário executivo.
    """
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
    summary_story.append(Spacer(1, 0.2 * inch))

    summary_story.append(Paragraph("Tom de Voz:", styles['SummaryTitle']))
    summary_story.append(Paragraph(weekly_strategy_summary.get('tone_of_voice', 'N/A'), styles['SummaryText']))
    summary_story.append(Spacer(1, 0.5 * inch))

    return summary_story