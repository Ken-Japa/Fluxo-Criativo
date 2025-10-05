import json
import os

class PromptManager:
    """
    Gerencia a construção de prompts otimizados para LLMs como o Google Gemini.
    """

    def __init__(self, client_profile: dict, niche_guidelines: dict):
        """
        Inicializa o PromptManager com o perfil do cliente e diretrizes do nicho.

        Args:
            client_profile (dict): Dicionário contendo o perfil do cliente (subnicho, tom_de_voz, publico_alvo, objetivos_gerais).
            niche_guidelines (dict): Dicionário contendo diretrizes específicas para o subnicho (restricoes_conteudo, exemplos_sucesso).
        """
        self.client_profile = client_profile
        self.niche_guidelines = niche_guidelines

    def build_prompt(self, content_type: str, weekly_themes: list[str], weekly_goal: str) -> str:
        """
        Constrói um prompt completo e otimizado para a IA gerar conteúdo.

        Args:
            content_type (str): Tipo de conteúdo desejado (ex: 'instagram_post', 'facebook_post').
            weekly_themes (list[str]): Lista de temas da semana.
            weekly_goal (str): Objetivo principal da semana (ex: 'aumentar engajamento').

        Returns:
            str: O prompt completo formatado para a API do Gemini.
        """
        # Coleta de dados do perfil do cliente e diretrizes do nicho, tratando valores vazios
        client_name = self.client_profile.get("client_name", "")
        subniche = self.client_profile.get("subniche", "")
        tom_de_voz = self.client_profile.get("tone_of_voice", "")
        public_target = self.client_profile.get("public_target", "")
        objetivos_gerais = self.client_profile.get("objetivos_gerais", "")
        niche_examples = self.client_profile.get("niche_examples", [])
        marketing_goals = self.client_profile.get("marketing_goals", "")
        distribution_channels = self.client_profile.get("distribution_channels", [])
        main_topics = self.client_profile.get("main_topics", [])
        keywords = self.client_profile.get("keywords", [])
        call_to_action = self.client_profile.get("call_to_action", "")
        restrictions_guidelines = self.client_profile.get("restrictions_guidelines", "")
        additional_info = self.client_profile.get("additional_info", "")
        competitors_references = self.client_profile.get("competitors_references", [])

        restricoes_conteudo = self.niche_guidelines.get("restricoes_conteudo", "")
        exemplos_sucesso = self.niche_guidelines.get("exemplos_sucesso", "")

        # System Message: Define o papel da IA
        system_message = f"Você é um copywriter especializado em mídias sociais."
        if subniche:
            system_message += f" para {subniche}."
        system_message += f" Seu objetivo é criar conteúdo altamente engajador e relevante para o público-alvo do cliente."

        # User Message: Combina todas as informações para criar uma instrução detalhada
        user_message_parts = [
            f"Com base no perfil do cliente e nas diretrizes do nicho, crie conteúdo para {content_type}."
        ]

        user_message_parts.append("\n**Perfil do Cliente:**")
        if client_name:
            user_message_parts.append(f"- Nome do Cliente: {client_name}")
        if subniche:
            user_message_parts.append(f"- Subnicho: {subniche}")
        if tom_de_voz:
            user_message_parts.append(f"- Tom de Voz: {tom_de_voz}")
        if public_target:
            user_message_parts.append(f"- Público-Alvo: {public_target}")
        if objetivos_gerais:
            user_message_parts.append(f"- Objetivos Gerais: {objetivos_gerais}")
        if niche_examples:
            user_message_parts.append(f"- Exemplos de Nicho: {', '.join(niche_examples)}")
        if marketing_goals:
            user_message_parts.append(f"- Objetivos de Marketing: {marketing_goals}")
        if distribution_channels:
            user_message_parts.append(f"- Canais de Distribuição: {', '.join(distribution_channels)}")
        if main_topics:
            user_message_parts.append(f"- Tópicos Principais: {', '.join(main_topics)}")
        if keywords:
            user_message_parts.append(f"- Palavras-Chave: {', '.join(keywords)}")
        if call_to_action:
            user_message_parts.append(f"- Chamada para Ação (CTA): {call_to_action}")
        if restrictions_guidelines:
            user_message_parts.append(f"- Restrições/Diretrizes: {restrictions_guidelines}")
        if additional_info:
            user_message_parts.append(f"- Informações Adicionais: {additional_info}")
        if competitors_references:
            user_message_parts.append(f"- Concorrentes/Referências: {', '.join(competitors_references)}")

        if restricoes_conteudo or exemplos_sucesso:
            user_message_parts.append("\n**Diretrizes do Nicho:**")
            if restricoes_conteudo:
                user_message_parts.append(f"- Restrições de Conteúdo: {restricoes_conteudo}")
            if exemplos_sucesso:
                user_message_parts.append(f"- Exemplos de Sucesso: {exemplos_sucesso}")

        if weekly_themes or weekly_goal:
            user_message_parts.append("\n**Contexto Semanal:**")
            if weekly_themes:
                user_message_parts.append(f"- Temas da Semana: {', '.join(weekly_themes)}")
            if weekly_goal:
                user_message_parts.append(f"- Objetivo Semanal: {weekly_goal}")

        user_message_parts.append("\n**Instruções de Formato:**")
        user_message_parts.append("Gere 5 ideias de posts. Para cada post, inclua:")
        user_message_parts.append("- `titulo`: Um título conciso para o post.")
        user_message_parts.append("- `legenda_principal`: A legenda principal do post.")
        user_message_parts.append("- `variacoes_legenda`: Uma lista de 2-3 variações da legenda principal.")
        user_message_parts.append("- `hashtags`: Uma lista de hashtags relevantes.")
        user_message_parts.append("- `sugestao_formato`: Sugestão de formato (ex: \"Carrossel de imagens\", \"Vídeo curto\", \"Infográfico\").")

        user_message_parts.append("\nRetorne o conteúdo em formato JSON, seguindo a estrutura abaixo:")
        user_message_parts.append("```json")
        user_message_parts.append("{{")
        user_message_parts.append("    \"posts\": [")
        user_message_parts.append("        {{")
        user_message_parts.append("            \"titulo\": \"Título do Post 1\",")
        user_message_parts.append("            \"legenda_principal\": \"Legenda principal do post 1.\",")
        user_message_parts.append("            \"variacoes_legenda\": [")
        user_message_parts.append("                \"Variação 1 da legenda 1.\",")
        user_message_parts.append("                \"Variação 2 da legenda 1.\"")
        user_message_parts.append("            ],")
        user_message_parts.append("            \"hashtags\": [\"#hashtag1\", \"#hashtag2\"],")
        user_message_parts.append("            \"sugestao_formato\": \"Carrossel de imagens\"")
        user_message_parts.append("        }},")
        user_message_parts.append("        // ... mais 4 posts ...")
        user_message_parts.append("    ]")
        user_message_parts.append("}}")
        user_message_parts.append("```")

        user_message = "\n".join(user_message_parts)

        return f"{system_message}\n\n{user_message}"

    def build_image_prompt(self, post_content: dict) -> str:
        """
        Constrói um prompt detalhado para uma IA de geração de imagens/vídeos com base no conteúdo do post.

        Args:
            post_content (dict): Dicionário contendo o conteúdo de um post (ex: legenda_principal, formato_sugerido).

        Returns:
            str: O prompt visual detalhado para a IA de geração de imagens.
        """
        client_name = self.client_profile.get('client_name', 'cliente')
        subniche = self.client_profile.get('subniche', 'geral')
        tone_of_voice = self.client_profile.get('tom_de_voz', 'neutro')
        public_target = self.client_profile.get('publico_alvo', 'amplo')

        main_caption = post_content.get('legenda_principal', '')
        suggested_format = post_content.get('sugestao_formato', '')

        prompt_parts = [
            f"Crie um prompt visual detalhado para uma IA de geração de imagens/vídeos.",
            f"O objetivo é gerar uma imagem ou vídeo que complemente o seguinte conteúdo de post para {client_name} (subnicho: {subniche}):",
            f"Legenda Principal: {main_caption}",
            f"Formato Sugerido: {suggested_format}",
            f"O tom de voz geral é {tone_of_voice} e o público-alvo é {public_target}.",
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
        "subnicho": "Nutrição Esportiva para Atletas de Endurance",
        "tom_de_voz": "Inspirador e Educativo",
        "publico_alvo": "Atletas amadores e profissionais de corrida e ciclismo",
        "objetivos_gerais": "Aumentar o desempenho, otimizar a recuperação e prevenir lesões"
    }

    # Exemplo de diretrizes do nicho
    niche_guidelines_example = {
        "restricoes_conteudo": "Evitar dietas extremas, foco em ciência e evidências.",
        "exemplos_sucesso": "Posts sobre hidratação, suplementação inteligente, nutrição pré/pós-treino."
    }

    prompt_manager = PromptManager(client_profile_example, niche_guidelines_example)

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