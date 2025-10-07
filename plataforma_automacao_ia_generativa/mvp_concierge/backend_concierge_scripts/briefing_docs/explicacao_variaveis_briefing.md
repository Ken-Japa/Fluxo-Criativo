# Explicação das Variáveis do Briefing e seu Impacto na Construção do Prompt da IA

Este documento descreve como cada variável do arquivo `client_briefing-clean.json` é utilizada na construção do prompt para a IA, conforme implementado no arquivo `build_prompt.py`.

## Variáveis e seus Impactos

1. **`nome_do_cliente`**
   - **Uso**: Incluído no perfil do cliente para personalização.
   - **Impacto**: Adiciona contexto personalizado ao prompt, ajudando a IA a se referir ao cliente de forma específica.

2. **`subnicho`**
   - **Uso**: Define o nicho de atuação do cliente.
   - **Impacto**: Influencia a mensagem do sistema (`system_message`) para contextualizar a IA sobre o nicho do cliente.

3. **`informacoes_de_contato`**
   - **Uso**: Não é utilizado diretamente no prompt.
   - **Impacto**: Pode ser usado para referência interna ou em futuras expansões do sistema.

4. **`publico_alvo`**
   - **Uso**: Descreve o público-alvo do cliente.
   - **Impacto**: Incluído no perfil do cliente para direcionar o conteúdo gerado para o público correto.

5. **`tom_de_voz`**
   - **Uso**: Define o tom de comunicação do cliente.
   - **Impacto**: Incluído no perfil do cliente para garantir que o conteúdo gerado siga o tom desejado.

6. **`estilo_de_comunicacao`**
   - **Uso**: Especifica o estilo de comunicação preferido.
   - **Impacto**: Direciona a IA para criar conteúdo alinhado ao estilo do cliente.

7. **`vocabulario_da_marca`**
   - **Uso**: Lista de palavras ou frases usadas pela marca.
   - **Impacto**: Incluído no perfil do cliente para adaptar o vocabulário do conteúdo gerado.

8. **`exemplos_de_nicho`**
   - **Uso**: Exemplos de referências no nicho.
   - **Impacto**: Usado para contextualizar a IA sobre o nicho e suas particularidades.

9. **`objetivos_de_marketing`**
   - **Uso**: Define os objetivos de marketing do cliente.
   - **Impacto**: Influencia a sugestão de métricas e o direcionamento do conteúdo.

10. **`canais_de_distribuicao`**
    - **Uso**: Lista de canais onde o conteúdo será distribuído.
    - **Impacto**: Direciona o conteúdo para os canais específicos, adaptando o formato e a linguagem.

11. **`topicos_principais`**
    - **Uso**: Tópicos principais a serem abordados.
    - **Impacto**: Garante que o conteúdo gerado aborde os temas relevantes para o cliente.

12. **`palavras_chave`**
    - **Uso**: Palavras-chave relevantes para o conteúdo.
    - **Impacto**: Usadas para otimizar o conteúdo para SEO e alinhamento com as estratégias do cliente.

13. **`chamada_para_acao`**
    - **Uso**: Define a chamada para ação (CTA) do conteúdo.
    - **Impacto**: Incluída no conteúdo gerado para direcionar o público a realizar uma ação específica.

14. **`restricoes_e_diretrizes`**
    - **Uso**: Restrições e diretrizes para o conteúdo.
    - **Impacto**: Limitações ou orientações específicas que a IA deve seguir ao gerar o conteúdo.

15. **`informacoes_adicionais`**
    - **Uso**: Informações extras relevantes.
    - **Impacto**: Adiciona contexto adicional ao conteúdo gerado.

16. **`referencias_de_concorrentes`**
    - **Uso**: Referências de concorrentes ou marcas similares.
    - **Impacto**: Usado para análise estratégica e diferenciação do conteúdo.

17. **`referencias_de_estilo_e_formato`**
    - **Uso**: Referências de estilo e formato de conteúdo.
    - **Impacto**: Direciona a IA para seguir estilos e formatos específicos.

18. **`tipo_de_conteudo`**
    - **Uso**: Tipo de conteúdo a ser gerado (ex: post de Instagram).
    - **Impacto**: Define o formato e a estrutura do conteúdo gerado.

19. **`tipo_de_campanha`**
    - **Uso**: Tipo de campanha (ex: autoridade).
    - **Impacto**: Influencia a sugestão de métricas e a narrativa da campanha.

20. **`posts_anteriores`**
    - **Uso**: Lista de posts anteriores do cliente.
    - **Impacto**: Usado para evitar repetições e garantir originalidade no conteúdo.

21. **`conteudos_semanais`**
    - **Uso**: Temas e objetivos semanais.
    - **Impacto**: Define o contexto semanal para a geração de conteúdo coeso e progressivo.

## Conclusão

Cada variável do briefing desempenha um papel específico na construção do prompt da IA, garantindo que o conteúdo gerado seja personalizado, relevante e alinhado com as necessidades do cliente.