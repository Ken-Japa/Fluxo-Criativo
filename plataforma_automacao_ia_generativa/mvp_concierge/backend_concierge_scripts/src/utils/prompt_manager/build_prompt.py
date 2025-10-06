import json

def build_prompt(client_profile: dict, niche_guidelines: dict, content_type: str, weekly_themes: list[str], weekly_goal: str, strategic_analysis: dict = None) -> str:
    """
    Constrói o prompt completo para a API do Gemini, combinando o perfil do cliente, diretrizes de nicho, contexto semanal e instruções de formato.

    Args:
        client_profile (dict): Dicionário contendo o perfil do cliente (subnicho, tom_de_voz, publico_alvo, objetivos_gerais).
        niche_guidelines (dict): Dicionário contendo diretrizes específicas do nicho.
        content_type (str): O tipo de conteúdo a ser gerado (ex: 'instagram_post').
        weekly_themes (list[str]): Uma lista de temas a serem abordados na semana.
        weekly_goal (str): O objetivo principal do conteúdo para a semana.
        strategic_analysis (dict): O resultado da análise estratégica do briefing.

    Returns:
        str: O prompt completo formatado para a API do Gemini.
    """

    # Coleta de dados do perfil do cliente e diretrizes do nicho, tratando valores vazios
    nome_do_cliente = client_profile.get("nome_do_cliente", "")
    subnicho = client_profile.get("subnicho", "")
    tom_de_voz = client_profile.get("tom_de_voz", "")
    publico_alvo = client_profile.get("publico_alvo", "")
    objetivos_de_marketing = client_profile.get("objetivos_de_marketing", "")
    exemplos_de_nicho = client_profile.get("exemplos_de_nicho", [])
    canais_de_distribuicao = client_profile.get("canais_de_distribuicao", [])
    topicos_principais = client_profile.get("topicos_principais", [])
    palavras_chave = client_profile.get("palavras_chave", [])
    chamada_para_acao = client_profile.get("chamada_para_acao", "")
    restricoes_e_diretrizes = client_profile.get("restricoes_e_diretrizes", "")
    informacoes_adicionais = client_profile.get("informacoes_adicionais", "")
    referencias_de_concorrentes = client_profile.get("referencias_de_concorrentes", [])
    referencias_de_estilo_e_formato = client_profile.get("referencias_de_estilo_e_formato", [])

    # Adicionar diretrizes de nicho, se existirem
    if niche_guidelines:
        for key, value in niche_guidelines.items():
            if isinstance(value, list):
                informacoes_adicionais += f" {key}: {', '.join(value)}."
            else:
                informacoes_adicionais += f" {key}: {value}."

    # System Message: Define o papel da IA
    system_message = f"Você é um copywriter especializado em mídias sociais."
    if subnicho:
        system_message += f" para {subnicho}."
    if niche_guidelines:
        system_message += f" Atuando sob as diretrizes de nicho: {json.dumps(niche_guidelines)}."
    system_message += f" Seu objetivo é criar conteúdo altamente engajador e relevante para o público-alvo do cliente."

    # User Message: Combina todas as informações para criar uma instrução detalhada
    user_message_parts = [
        f"Com base no perfil do cliente e nas diretrizes do nicho, crie conteúdo para {content_type}."
    ]

    user_message_parts.append("\n**Perfil do Cliente:**")
    if nome_do_cliente:
        user_message_parts.append(f"- Nome do Cliente: {nome_do_cliente}")
    if subnicho:
        user_message_parts.append(f"- Subnicho: {subnicho}")
    if tom_de_voz:
        user_message_parts.append(f"- Tom de Voz: {tom_de_voz}")
    if publico_alvo:
        user_message_parts.append(f"- Público-Alvo: {publico_alvo}")

    # Análise Estratégica Inicial
    user_message_parts.append("\n**Análise Estratégica Inicial:**")
    if subnicho:
        user_message_parts.append(f"- Contexto do Subnicho: O cliente atua no subnicho de {subnicho}. Compreenda as nuances e particularidades deste segmento para gerar conteúdo altamente relevante.")
    if referencias_de_concorrentes:
        user_message_parts.append(f"- Análise de Concorrentes/Referências: Considere o estilo e as estratégias de conteúdo dos seguintes concorrentes/referências: {', '.join(referencias_de_concorrentes)}. Identifique oportunidades e diferenciais.")
    if informacoes_adicionais:
        user_message_parts.append(f"- Informações Adicionais e Diretrizes Específicas: {informacoes_adicionais}. Incorpore essas informações para refinar a estratégia de conteúdo.")

    if strategic_analysis:
        user_message_parts.append("\n**Informações Estratégicas do Briefing:**")
        for key, value in strategic_analysis.items():
            if value and value != "Não especificado": # Adiciona apenas se o valor não for vazio ou 'Não especificado'
                if isinstance(value, list):
                    user_message_parts.append(f"- {key.replace('_', ' ').title()}: {', '.join(value)}")
                else:
                    user_message_parts.append(f"- {key.replace('_', ' ').title()}: {value}")

    if objetivos_de_marketing:
        user_message_parts.append(f"- Objetivos de Marketing: {objetivos_de_marketing}")
    if exemplos_de_nicho:
        user_message_parts.append(f"- Exemplos de Nicho: {', '.join(exemplos_de_nicho)}")
    if canais_de_distribuicao:
        user_message_parts.append(f"- Canais de Distribuição: {', '.join(canais_de_distribuicao)}")
    if topicos_principais:
        user_message_parts.append(f"- Tópicos Principais: {', '.join(topicos_principais)}")
    if palavras_chave:
        user_message_parts.append(f"- Palavras-Chave: {', '.join(palavras_chave)}")
    if chamada_para_acao:
        user_message_parts.append(f"- Chamada para Ação (CTA): {chamada_para_acao}")
    if restricoes_e_diretrizes:
        user_message_parts.append(f"- Restrições e Diretrizes: {restricoes_e_diretrizes}")
    if informacoes_adicionais:
        user_message_parts.append(f"- Informações Adicionais: {informacoes_adicionais}")
    if referencias_de_concorrentes:
        user_message_parts.append(f"- Concorrentes/Referências: {', '.join(referencias_de_concorrentes)}")
    if referencias_de_estilo_e_formato:
        user_message_parts.append(f"- Referências de Estilo e Formato: {', '.join(referencias_de_estilo_e_formato)}")

    if weekly_themes or weekly_goal:
        user_message_parts.append("\n**Contexto Semanal:**")
        if weekly_themes:
            user_message_parts.append(f"- Temas da Semana: {', '.join(weekly_themes)}")
        if weekly_goal:
            user_message_parts.append(f"- Objetivo Semanal: {weekly_goal}")

    user_message_parts.append("\n**Instruções de Formato:**")
    user_message_parts.append("Crie uma campanha semanal *coesa e com narrativa progressiva*, composta por 5 ideias de posts. Para cada post, inclua:")
    user_message_parts.append("A campanha deve seguir uma narrativa progressiva ao longo dos 5 posts, abordando:")
    user_message_parts.append("- Post 1: Apresentação do Problema/Desafio do público-alvo.")
    user_message_parts.append("- Post 2: Introdução da Solução (produto/serviço do cliente).")
    user_message_parts.append("- Post 3: Detalhamento dos Benefícios e Vantagens da solução.")
    user_message_parts.append("- Post 4: Prova Social/Exemplos de Sucesso/Depoimentos.")
    user_message_parts.append("- Post 5: Chamada para Ação (CTA) clara e direta.")
    user_message_parts.append("- `titulo`: Um título conciso para o post.")
    user_message_parts.append("- `legenda_principal`: A legenda principal do post.")
    user_message_parts.append("- `variacoes_legenda`: Uma lista de 2-3 variações da legenda principal.")
    user_message_parts.append("- `hashtags`: Uma lista de hashtags relevantes.")
    user_message_parts.append("- `sugestao_formato`: Sugestão de formato (ex: \"Carrossel de imagens\", \"Vídeo curto\", \"Infográfico\").")
    user_message_parts.append("- `post_strategy_rationale`: Uma justificativa estratégica detalhada para este post, explicando como ele se encaixa na narrativa semanal e contribui para os objetivos gerais.")
    user_message_parts.append("- `micro_briefing`: Um breve resumo do objetivo e foco principal do post, para contextualização.")
    user_message_parts.append("- `micro_roteiro`: Se `sugestao_formato` for \"Vídeo curto\" ou \"Reel\", inclua um micro-roteiro detalhando cenas, falas/textos e chamadas para ação.")
    user_message_parts.append("- `carrossel_slides`: Se `sugestao_formato` for \"Carrossel de imagens\", inclua uma lista de objetos, onde cada objeto representa um slide do carrossel, contendo `titulo_slide`, `texto_slide` e `sugestao_visual_slide`.")
    user_message_parts.append("- `visual_prompt_suggestion`: Uma descrição detalhada da imagem ou vídeo principal para o post, incluindo estilo, cores, elementos e atmosfera, para ser usada por uma IA de geração de imagens.")

    user_message_parts.append("\nRetorne o conteúdo em formato JSON, seguindo a estrutura abaixo:")
    user_message_parts.append("```json")
    user_message_parts.append("{{")
    user_message_parts.append("    \"weekly_strategy_summary\": \"Resumo da estratégia semanal para a campanha.\",")
    user_message_parts.append("    \"posts\": [")
    user_message_parts.append("        {{")
    user_message_parts.append("            \"titulo\": \"Título do Post 1\",")
    user_message_parts.append("            \"legenda_principal\": \"Legenda principal do post 1.\",")
    user_message_parts.append("            \"variacoes_legenda\": [")
    user_message_parts.append("                \"Variação 1 da legenda 1.\",")
    user_message_parts.append("                \"Variação 2 da legenda 1.\"")
    user_message_parts.append("            ],")
    user_message_parts.append("            \"hashtags\": [\"#Hashtag1\", \"#Hashtag2\"],")
    user_message_parts.append("            \"sugestao_formato\": \"Carrossel de imagens\",")
    user_message_parts.append("            \"post_strategy_rationale\": \"Justificativa estratégica para este post.\",")
    user_message_parts.append("            \"micro_briefing\": \"Breve resumo do objetivo do post.\",")
    user_message_parts.append("            \"visual_prompt_suggestion\": \"Descrição detalhada para IA de geração de imagens.\",")
    user_message_parts.append("            \"micro_roteiro\": [")
    user_message_parts.append("                {")
    user_message_parts.append("                    \"cena\": 1,")
    user_message_parts.append("                    \"descricao\": \"Pessoa sorrindo\",")
    user_message_parts.append("                    \"texto_tela\": \"Problema resolvido!\",")
    user_message_parts.append("                    \"fala\": \"Você sabia que...?\"")
    user_message_parts.append("                }")
    user_message_parts.append("            ],")
    user_message_parts.append("            \"carrossel_slides\": [")
    user_message_parts.append("                {")
    user_message_parts.append("                    \"titulo_slide\": \"Título do Slide 1\",")
    user_message_parts.append("                    \"texto_slide\": \"Texto do slide 1\",")
    user_message_parts.append("                    \"sugestao_visual_slide\": \"Visual para slide 1\"")
    user_message_parts.append("                }")
    user_message_parts.append("            ]")
    user_message_parts.append("        }}")
    user_message_parts.append("    ]")
    user_message_parts.append("}}")
    user_message_parts.append("```")

    user_message = "\n".join(user_message_parts)

    return f"{system_message}\n\n{user_message}"