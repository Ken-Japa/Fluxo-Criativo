# Guia de Preenchimento do client_briefing.json

Este guia descreve cada campo no arquivo `client_briefing.json` e oferece sugestões para seu preenchimento, visando otimizar a geração de conteúdo.

## Estrutura do JSON

```json
{
  "nome_do_cliente": "",
  "subnicho": "",
  "informacoes_de_contato": "",
  "publico_alvo": "",
  "tom_de_voz": "",
  "exemplos_de_nicho": [],
  "objetivos_de_marketing": "",
  "canais_de_distribuicao": [],
  "topicos_principais": [],
  "palavras_chave": [],
  "chamada_para_acao": "",
   "restricoes_e_diretrizes": "",
  "informacoes_adicionais": "",
  "referencias_de_concorrentes": [],
  "referencias_de_estilo_e_formato": [],
  "tipo_de_conteudo": [],
  "conteudos_semanais": []
}
```

## Descrição dos Campos

### `nome_do_cliente` (String)
*   **Descrição**: Nome completo ou comercial do cliente/empresa para quem o conteúdo será gerado.
*   **Obrigatório**: Sim. Essencial para identificar o cliente e personalizar o conteúdo.
*   **Impacto**: Usado para identificação no PDF/HTML e para a IA manter o contexto da marca.
*   **Melhor Referência**: "PetShop Fofura Animal", "Clínica Veterinária Saúde & Cia", "Escola de Idiomas Global".

### `subnicho` (String)
*   **Descrição**: Uma descrição mais específica do nicho de atuação do cliente.
*   **Obrigatório**: Sim. Crucial para a IA focar no segmento específico do cliente.
*   **Impacto**: Guia a IA na geração de conteúdo relevante e específico. Aparece no briefing do PDF/HTML.
*   **Melhor Referência**: "Venda de produtos premium para cães e gatos com foco em bem-estar", "Serviços veterinários especializados em ortopedia e fisioterapia animal", "Cursos de inglês online para profissionais de TI".

### `informacoes_de_contato` (String)
*   **Descrição**: E-mail ou telefone de contato principal do cliente.
*   **Obrigatório**: Não (Opcional). Pode ser útil para referência, mas não afeta diretamente a geração do conteúdo.
*   **Impacto**: Pode ser incluído no PDF/HTML para contato, mas não influencia o conteúdo gerado pela IA.
*   **Melhor Referência**: "contato@petshopfofura.com.br", "(11) 98765-4321", "www.escolaglobal.com/contato".

### `publico_alvo` (String)
*   **Descrição**: Descrição detalhada do público que o cliente deseja alcançar. Inclua dados demográficos, interesses, dores e aspirações.
*   **Obrigatório**: Sim. Fundamental para a IA adaptar a linguagem, o tom e os temas ao público desejado.
*   **Impacto**: Essencial para a IA direcionar o conteúdo de forma eficaz. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: "Donos de cães e gatos, classe B/A, entre 25-55 anos, que consideram seus pets membros da família, buscam produtos de alta qualidade, orgânicos e sustentáveis, e valorizam a saúde e longevidade de seus animais. Preocupam-se com a origem dos produtos e a ética das marcas."

### `tom_de_voz` (String)
*   **Descrição**: O estilo e a personalidade que o conteúdo deve transmitir.
*   **Obrigatório**: Sim. Guia a IA na escolha da linguagem, personalidade e estilo de comunicação.
*   **Impacto**: Direciona o estilo do conteúdo gerado. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: "Empático, acolhedor e informativo, com um toque de humor leve e carinhoso. Evitar jargões técnicos excessivos, mas manter a autoridade no assunto."
*   **Sugestões Adicionais**: "Inspirador e motivacional", "Direto e objetivo", "Amigável e acessível", "Luxuoso e exclusivo", "Jovem e descolado".

### `exemplos_de_nicho` (Array de Strings)
*   **Descrição**: Exemplos de tópicos ou áreas de conteúdo que o cliente já aborda ou gostaria de abordar.
*   **Obrigatório**: Não (Opcional, mas altamente recomendado). Fornece exemplos concretos de tópicos para a IA.
*   **Impacto**: Ajuda a IA a entender melhor o escopo e a profundidade dos temas. Não aparece no conteúdo final, mas sim no briefing.
*   **Melhor Referência**: `["Nutrição natural para pets", "Adestramento positivo de cães", "Benefícios da acupuntura em gatos", "Tendências de moda pet sustentável", "Dicas de viagem com animais de estimação"]`

### `objetivos_de_marketing` (String)
*   **Descrição**: Os principais objetivos que o cliente espera alcançar com o conteúdo gerado.
*   **Obrigatório**: Sim. A IA precisa saber o propósito do conteúdo para otimizá-lo para resultados.
*   **Impacto**: Guia a IA na criação de conteúdo com foco em metas específicas. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: "Aumentar o reconhecimento da marca em 30% nos próximos 6 meses, gerar 500 leads qualificados por mês para a linha de produtos orgânicos, e aumentar as vendas online em 15% no próximo trimestre. Posicionar a marca como líder em bem-estar animal."

### `canais_de_distribuicao` (Array de Strings)
*   **Descrição**: Plataformas ou veículos **onde** o conteúdo será publicado. Isso define o ambiente de distribuição.
*   **Obrigatório**: Sim. Influencia o formato, a extensão e o estilo do conteúdo, pois cada canal tem suas particularidades.
*   **Impacto**: A IA pode adaptar o conteúdo para cada canal. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: `["Instagram (Stories, Reels, Feed)", "Blog (SEO-friendly)", "YouTube (tutoriais e vlogs)", "Newsletter por e-mail", "Facebook Ads (retargeting)"]`
*   **Sugestões Adicionais**: `["LinkedIn (para B2B)", "TikTok (conteúdo rápido e divertido)", "Pinterest (infográficos e inspiração)"]`

### `topicos_principais` (Array de Strings)
*   **Descrição**: Temas centrais que devem ser abordados no conteúdo.
*   **Obrigatório**: Sim. Define os temas gerais que devem ser abordados no conteúdo.
*   **Impacto**: Ajuda a IA a manter o foco nos temas centrais. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: `["Alimentação saudável para pets", "Saúde preventiva e bem-estar animal", "Comportamento e adestramento", "Produtos inovadores e sustentáveis para pets", "Histórias inspiradoras de pets e seus donos"]`

### `palavras_chave` (Array de Strings)
*   **Descrição**: Palavras e frases-chave relevantes para o SEO e a busca do público.
*   **Obrigatório**: Sim (se o objetivo incluir SEO). Essencial para a IA otimizar o conteúdo para busca.
*   **Impacto**: A IA incorporará essas palavras-chave para melhorar a visibilidade do conteúdo. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: `["ração natural para cães", "petiscos orgânicos gatos", "veterinário holístico", "acessórios pet ecológicos", "adestramento filhotes", "ansiedade separação cães"]`

### `chamada_para_acao` (String - Opcional)
*   **Descrição**: A ação que se espera que o público realize após consumir o conteúdo. Se não for fornecida, a IA poderá sugerir a CTA mais adequada com base no contexto.
*   **Obrigatório**: Não (Opcional). A IA pode decidir qual o melhor CTA para o tipo de conteúdo e canal de distribuição.
*   **Impacto**: A IA incluirá a CTA no conteúdo gerado. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: "Compre agora e garanta 10% de desconto na primeira compra!", "Agende uma consulta gratuita com nossos especialistas!", "Baixe nosso e-book exclusivo sobre nutrição pet!", "Visite nosso site para conhecer a linha completa!".### `restricoes_e_diretrizes` (String)
*   **Descrição**: Quaisquer restrições de linguagem, estilo, temas a serem evitados ou diretrizes específicas da marca.
*   **Obrigatório**: Não (Opcional, mas altamente recomendado). Ajuda a IA a evitar erros e desalinhamentos com a marca.
*   **Impacto**: Guia a IA sobre o que evitar em termos de linguagem, estilo ou temas. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: "Evitar termos que possam gerar pânico ou culpa nos donos de pets. Não usar imagens de animais em situações de estresse. Manter a linguagem inclusiva e respeitosa. Não mencionar marcas concorrentes diretamente."

### `informacoes_adicionais` (String)
*   **Descrição**: Qualquer outra informação relevante que possa ajudar na criação do conteúdo.
*   **Obrigatório**: Não (Opcional). Para informações extras que não se encaixam em outros campos.
*   **Impacto**: Pode fornecer contexto adicional valioso para a IA. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: "Temos uma nova linha de brinquedos interativos para cães de grande porte que será lançada no próximo mês. Focar nos benefícios para a saúde mental e física dos animais. O CEO da empresa é um veterinário renomado e pode ser citado como fonte."

### `referencias_de_concorrentes` (Array de Strings)
*   **Descrição**: Nomes ou links de concorrentes que o cliente admira ou deseja se diferenciar.
*   **Obrigatório**: Não (Opcional, mas útil). Ajuda a IA a entender o cenário competitivo e a posicionar o conteúdo.
*   **Impacto**: A IA pode usar essas referências para diferenciar o conteúdo. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: `["Petz (analisar estratégias de e-commerce)", "Zee.Dog (observar tom de voz e design)", "Royal Canin (entender posicionamento em nutrição)"]`

### `referencias_de_estilo_e_formato` (Array de Strings)
*   **Descrição**: URLs ou descrições de exemplos de conteúdo que o cliente admira em termos de estilo, formatação, design visual, tom, etc. Isso ajuda a IA a entender a estética desejada.
*   **Obrigatório**: Não (Opcional, mas altamente recomendado). Guia a IA na estética e no design desejado.
*   **Impacto**: Ajuda a IA a replicar um estilo visual e de formatação específico. Exibido no briefing do PDF/HTML.
*   **Melhor Referência**: `["https://www.exemplo.com/blog/post-inspirador", "Tom de voz similar ao da marca X no Instagram", "Layout de blog minimalista e com muitas imagens, como o site Y"]`

### `tipo_de_conteudo` (Array de Strings)
*   **Descrição**: Os **formatos gerais** ou categorias de conteúdo a serem gerados (ex: post de blog, vídeo, infográfico). Permite especificar múltiplos tipos de conteúdo.
*   **Obrigatório**: Sim. Define os tipos gerais de conteúdo que o cliente deseja produzir.
*   **Impacto**: Crítico. Este campo informa à IA sobre os formatos de conteúdo esperados em um nível macro. Embora `tipo_de_conteudo_individual` seja mais específico para cada post, este campo pode ser usado para um entendimento geral do perfil de conteúdo do cliente. No PDF/HTML, pode listar os tipos de conteúdo que o cliente costuma trabalhar.
*   **Melhor Referência**: `["instagram_post (com foco em carrossel de dicas e Reels de demonstração de produtos)", "blog_post (artigos de 800-1200 palavras com SEO otimizado)", "youtube_script (reviews de produtos e entrevistas com veterinários)"]`
*   **Sugestões Adicionais**: `["email_marketing (sequência de boas-vindas e promoções)", "facebook_ad (vídeos curtos e chamativos)", "linkedin_post (artigos sobre empreendedorismo no mercado pet)", "tiktok_script (desafios e tendências com pets)"]`

### `conteudos_semanais` (Array de Objetos - Opcional)
*   **Descrição**: Uma lista de objetos, onde cada objeto representa um "mini-briefing" para um conteúdo específico a ser gerado na semana. Isso permite granularidade para cada post. Se não for fornecido, a IA pode gerar sugestões de conteúdo com base nos outros campos do briefing.
*   **Estrutura de cada objeto em `conteudos_semanais`**:
    ```json
    {
      "tema_do_conteudo": "",
      "tipo_de_conteudo_individual": [],
      "chamada_para_acao_individual": "" (Opcional),
      "objetivo_do_conteudo_individual": "" (Opcional),
      "tamanho_estimado_do_conteudo": ""
    }
    ```
*   **Melhor Referência (Exemplo de um objeto)**:
    ```json
    {
      "tema_do_conteudo": "Benefícios da alimentação natural para cães idosos",
      "tipo_de_conteudo_individual": `["instagram_post (carrossel)", "blog_post"]` (Opcional),
      "chamada_para_acao_individual": "Deslize para o lado e descubra como prolongar a vida do seu pet!" (Opcional),
      "objetivo_do_conteudo_individual": "Educar o público sobre alimentação natural e direcionar tráfego para o blog." (Opcional),
      "tamanho_estimado_do_conteudo": "5 slides de carrossel"
    }
    ```
*   **Sugestões Adicionais para `tema_do_conteudo`**: "Dicas de adestramento para filhotes", "Como escolher a melhor coleira para seu gato", "Histórias de sucesso de pets adotados".
*   **Sugestões Adicionais para `tipo_de_conteudo_individual`**: "facebook_post", "blog_post", "youtube_short", "tiktok_video".
*   **Sugestões Adicionais para `chamada_para_acao_individual`**: "Clique no link da bio para saber mais!", "Marque um amigo que precisa ver isso!", "Deixe seu comentário abaixo!".
*   **Sugestões Adicionais para `objetivo_do_conteudo_individual`**: "Aumentar o engajamento", "Gerar leads", "Promover um produto específico", "Construir autoridade da marca".
*   **Sugestões Adicionais para `tamanho_estimado_do_conteudo`**: "200-300 palavras", "1 minuto de vídeo", "1000 caracteres", "30 segundos de áudio".