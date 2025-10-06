import json
import os

class PromptManager:
    """
    Gerencia a construção de prompts otimizados para LLMs como o Google Gemini.
    """

    def __init__(self, client_profile: dict, niche_guidelines: dict = None):
        """
        Inicializa o PromptManager com o perfil do cliente e diretrizes de nicho.

        Args:
            client_profile (dict): Dicionário contendo o perfil do cliente (subnicho, tom_de_voz, publico_alvo, objetivos_gerais).
            niche_guidelines (dict): Dicionário contendo diretrizes específicas do nicho.
        """
        self.client_profile = client_profile
        self.niche_guidelines = niche_guidelines if niche_guidelines is not None else {}

    def build_prompt(self, content_type: str, weekly_themes: list[str], weekly_goal: str, briefing_content: str = None) -> str:
        """
        Constrói um prompt completo e otimizado para a IA gerar conteúdo.

        Args:
            content_type (str): Tipo de conteúdo desejado (ex: 'instagram_post', 'facebook_post').
            weekly_themes (list[str]): Lista de temas da semana.
            weekly_goal (str): Objetivo principal da semana (ex: 'aumentar engajamento').
            briefing_content (str): Conteúdo completo do briefing para análise estratégica.

        Returns:
            str: O prompt completo formatado para a API do Gemini.
        """
        strategic_info = {}
        if briefing_content:
            strategic_info = self.analyze_briefing_for_strategy(briefing_content)

        # Coleta de dados do perfil do cliente e diretrizes do nicho, tratando valores vazios
        nome_do_cliente = self.client_profile.get("nome_do_cliente", "")
        subnicho = self.client_profile.get("subnicho", "")
        tom_de_voz = self.client_profile.get("tom_de_voz", "")
        publico_alvo = self.client_profile.get("publico_alvo", "")
        objetivos_de_marketing = self.client_profile.get("objetivos_de_marketing", "")
        exemplos_de_nicho = self.client_profile.get("exemplos_de_nicho", [])
        canais_de_distribuicao = self.client_profile.get("canais_de_distribuicao", [])
        topicos_principais = self.client_profile.get("topicos_principais", [])
        palavras_chave = self.client_profile.get("palavras_chave", [])
        chamada_para_acao = self.client_profile.get("chamada_para_acao", "")
        restricoes_e_diretrizes = self.client_profile.get("restricoes_e_diretrizes", "")
        informacoes_adicionais = self.client_profile.get("informacoes_adicionais", "")
        referencias_de_concorrentes = self.client_profile.get("referencias_de_concorrentes", [])
        referencias_de_estilo_e_formato = self.client_profile.get("referencias_de_estilo_e_formato", [])

        # Adicionar diretrizes de nicho, se existirem
        if self.niche_guidelines:
            for key, value in self.niche_guidelines.items():
                if isinstance(value, list):
                    informacoes_adicionais += f" {key}: {', '.join(value)}."
                else:
                    informacoes_adicionais += f" {key}: {value}."

        # System Message: Define o papel da IA
        system_message = f"Você é um copywriter especializado em mídias sociais."
        if subnicho:
            system_message += f" para {subnicho}."
        if self.niche_guidelines:
            system_message += f" Atuando sob as diretrizes de nicho: {json.dumps(self.niche_guidelines)}."
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

        if strategic_info:
            user_message_parts.append("\n**Informações Estratégicas do Briefing:**")
            for key, value in strategic_info.items():
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
        user_message_parts.append("Crie uma campanha semanal coesa, composta por 5 ideias de posts. Para cada post, inclua:")
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
        user_message_parts.append("- `micro_briefing`: Um breve resumo do objetivo e foco principal do post, para contextualização.")
        user_message_parts.append("- `micro_roteiro`: Se `sugestao_formato` for \"Vídeo curto\" ou \"Reel\", inclua um micro-roteiro detalhando cenas, falas/textos e chamadas para ação.")
        user_message_parts.append("- `carrossel_slides`: Se `sugestao_formato` for \"Carrossel de imagens\", inclua uma lista de objetos, onde cada objeto representa um slide do carrossel, contendo `titulo_slide`, `texto_slide` e `sugestao_visual_slide`.")
        user_message_parts.append("- `sugestao_visual_geral`: Uma descrição detalhada da imagem ou vídeo principal para o post, incluindo estilo, cores, elementos e atmosfera, para ser usada por uma IA de geração de imagens.")

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
        user_message_parts.append("            \"hashtags\": [\"#hashtag1\", \"#hashtag2\"],")
        user_message_parts.append("            \"sugestao_formato\": \"Carrossel de imagens\",")
        user_message_parts.append("            \"post_strategy_rationale\": \"Justificativa estratégica para este post específico, alinhada aos objetivos da campanha.\",")
        user_message_parts.append("            \"micro_briefing\": \"Objetivo: Apresentar o problema X e gerar curiosidade.\",")
        user_message_parts.append("            \"carrossel_slides\": [")
        user_message_parts.append("                {{\"titulo_slide\": \"Título Slide 1\", \"texto_slide\": \"Texto do slide 1\", \"sugestao_visual_slide\": \"Imagem de X\"}},")
        user_message_parts.append("                {{\"titulo_slide\": \"Título Slide 2\", \"texto_slide\": \"Texto do slide 2\", \"sugestao_visual_slide\": \"Imagem de Y\"}}")
        user_message_parts.append("            ],")
        user_message_parts.append("            \"sugestao_visual_geral\": \"Descrição detalhada da imagem ou vídeo principal para o post, estilo, cores, elementos e atmosfera.\"")
        user_message_parts.append("        }}")
        user_message_parts.append("    ]")
        user_message_parts.append("}}")
        user_message_parts.append("```")

        user_message = "\n".join(user_message_parts)

        return f"{system_message}\n\n{user_message}"

    def analyze_briefing_for_strategy(self, briefing_content: str) -> dict:
        """
        Analisa o conteúdo de um briefing para extrair informações estratégicas.
        Este método simula a análise de um briefing para identificar elementos chave
        que podem ser usados para otimizar a geração de prompts.

        Args:
            briefing_content (str): O conteúdo completo do briefing a ser analisado.

        Returns:
            dict: Um dicionário contendo as informações estratégicas extraídas,
                  como objetivos, público-alvo, tom de voz, etc.
        """
        # Implementação real: Usar regex ou processamento de texto para extrair informações
        strategic_info = {
            "objetivos_estrategicos": "Não especificado",
            "publico_alvo_detalhado": "Não especificado",
            "tom_de_voz": "Não especificado",
            "palavras_chave": "Não especificado",
            "referencias_de_estilo": "Não especificado",
            "canais_de_distribuicao": "Não especificado",
            "restricoes_legais": "Não especificado",
            "orçamento_disponivel": "Não especificado",
            "cronograma_desejado": "Não especificado",
            "metricas_de_sucesso": "Não especificado",
            "informacoes_adicionais": "Não especificado"
        }

        # Exemplo de extração simples por palavras-chave
        briefing_lower = briefing_content.lower()

        if "objetivos:" in briefing_lower:
            start = briefing_lower.find("objetivos:") + len("objetivos:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["objetivos_estrategicos"] = briefing_content[start:end].strip()

        if "público-alvo:" in briefing_lower:
            start = briefing_lower.find("público-alvo:") + len("público-alvo:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["publico_alvo_detalhado"] = briefing_content[start:end].strip()

        if "tom de voz:" in briefing_lower:
            start = briefing_lower.find("tom de voz:") + len("tom de voz:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["tom_de_voz"] = briefing_content[start:end].strip()

        if "palavras-chave:" in briefing_lower:
            start = briefing_lower.find("palavras-chave:") + len("palavras-chave:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["palavras_chave"] = [kw.strip() for kw in briefing_content[start:end].split(',') if kw.strip()]

        if "referências de estilo:" in briefing_lower:
            start = briefing_lower.find("referências de estilo:") + len("referências de estilo:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["referencias_de_estilo"] = briefing_content[start:end].strip()

        if "canais de distribuição:" in briefing_lower:
            start = briefing_lower.find("canais de distribuição:") + len("canais de distribuição:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["canais_de_distribuicao"] = [c.strip() for c in briefing_content[start:end].split(',') if c.strip()]

        if "restrições legais:" in briefing_lower:
            start = briefing_lower.find("restrições legais:") + len("restrições legais:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["restricoes_legais"] = briefing_content[start:end].strip()

        if "orçamento disponível:" in briefing_lower:
            start = briefing_lower.find("orçamento disponível:") + len("orçamento disponível:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["orçamento_disponivel"] = briefing_content[start:end].strip()

        if "cronograma desejado:" in briefing_lower:
            start = briefing_lower.find("cronograma desejado:") + len("cronograma desejado:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["cronograma_desejado"] = briefing_content[start:end].strip()

        if "métricas de sucesso:" in briefing_lower:
            start = briefing_lower.find("métricas de sucesso:") + len("métricas de sucesso:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["metricas_de_sucesso"] = [m.strip() for m in briefing_content[start:end].split(',') if m.strip()]

        if "informações adicionais:" in briefing_lower:
            start = briefing_lower.find("informações adicionais:") + len("informações adicionais:")
            end = briefing_lower.find("\n", start)
            if end == -1: end = len(briefing_lower)
            strategic_info["informacoes_adicionais"] = briefing_content[start:end].strip()

        return strategic_info

    def build_image_prompt(self, post_content: dict) -> str:
        """
        Constrói um prompt detalhado para uma IA de geração de imagens/vídeos com base no conteúdo do post.

        Args:
            post_content (dict): Dicionário contendo o conteúdo de um post (ex: legenda_principal, formato_sugerido).

        Returns:
            str: O prompt visual detalhado para a IA de geração de imagens.
        """
        nome_do_cliente = self.client_profile.get('nome_do_cliente', 'cliente')
        subnicho = self.client_profile.get('subnicho', 'geral')
        tom_de_voz = self.client_profile.get('tom_de_voz', 'neutro')
        publico_alvo = self.client_profile.get('publico_alvo', 'amplo')

        main_caption = post_content.get('legenda_principal', '')
        suggested_format = post_content.get('sugestao_formato', '')

        prompt_parts = [
            f"Crie um prompt visual detalhado para uma IA de geração de imagens/vídeos.",
            f"O objetivo é gerar uma imagem ou vídeo que complemente o seguinte conteúdo de post para {nome_do_cliente} (subnicho: {subnicho}):",
            f"Legenda Principal: {main_caption}",
            f"Formato Sugerido: {suggested_format}",
            f"O tom de voz geral é {tom_de_voz} e o público-alvo é {publico_alvo}.",
            "Considere os seguintes elementos para o prompt visual:",
            "- Cenário e ambiente (interno/externo, dia/noite, localização específica).",
            "- Elementos visuais principais (pessoas, objetos, paisagens).",
            "- Estilo artístico (realista, cartoon, ilustração, 3D, fotografia).",
            "- Cores e iluminação (paleta de cores, tipo de luz).",
            "- Emoções e atmosfera que a imagem deve transmitir.",
            "- Composição e enquadramento (close-up, plano geral, ângulo).",
            "- Qualquer texto ou sobreposição que possa ser incluído na imagem (se aplicável).",
            "O prompt deve ser conciso, claro e rico em detalhes descritivos para guiar a IA de imagem/vídeo."
        ]

        return "\n".join(prompt_parts)


    def get_token_count(self, prompt_text: str) -> int:
        """
        Estima o número de tokens de um prompt. Esta é uma estimativa simples
        baseada no número de palavras.

        Args:
            prompt_text (str): O texto do prompt.

        Returns:
            int: Número estimado de tokens.
        """
        # Uma estimativa simples: 1 token ~ 4 caracteres ou 0.75 palavras
        # Para maior precisão, seria necessário usar um tokenizador específico do modelo.
        return len(prompt_text.split()) # Contagem de palavras como estimativa

# Exemplo de uso (para demonstração)
if __name__ == "__main__":
    # Exemplo de perfil do cliente
    client_profile_example = {
        "nome_do_cliente": "Empresa Exemplo",
        "subnicho": "Nutrição Esportiva para Atletas de Endurance",
        "tom_de_voz": "Inspirador e Educativo",
        "publico_alvo": "Atletas amadores e profissionais de corrida e ciclismo",
        "objetivos_de_marketing": "Aumentar o desempenho, otimizar a recuperação e prevenir lesões",
        "exemplos_de_nicho": ["Posts sobre hidratação", "suplementação inteligente", "nutrição pré/pós-treino."],
        "restricoes_e_diretrizes": "Evitar dietas extremas, foco em ciência e evidências."
    }

    prompt_manager = PromptManager(client_profile_example)

    content_type_example = "instagram_post"
    weekly_themes_example = ["Hidratação no Verão", "Recuperação Muscular", "Alimentação Pré-Treino"]
    weekly_goal_example = "Educar sobre a importância da hidratação e nutrição para o desempenho"

    generated_prompt = prompt_manager.build_prompt(
        content_type_example,
        weekly_themes_example,
        weekly_goal_example
    )

    print("--- Prompt Gerado ---")
    print(generated_prompt)
    print("\n--- Estimativa de Tokens ---")
    print(f"Tokens estimados: {prompt_manager.get_token_count(generated_prompt)}")

    # Para testar o carregamento da API Key (apenas para demonstração, não executa a API real aqui)
    # from dotenv import load_dotenv
    # load_dotenv()
    # api_key = os.getenv("GEMINI_API_KEY")
    # print(f"API Key carregada (se .env existir): {api_key}")