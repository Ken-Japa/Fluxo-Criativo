# MVP Concierge - Plataforma de Automação de Conteúdo com IA Generativa

## Descrição
O MVP Concierge é uma plataforma projetada para automatizar a geração de briefings de conteúdo personalizados para clientes, utilizando inteligência artificial generativa. O objetivo principal é otimizar o processo de criação de conteúdo, desde a coleta de informações do cliente até a entrega de um briefing detalhado em formatos HTML e PDF, que pode incluir sugestões de posts para redes sociais, ideias visuais e hashtags.

## Funcionalidades
- **Coleta de Briefing**: Um conjunto de perguntas estruturadas para coletar informações essenciais do cliente e suas necessidades de conteúdo.
- **Geração de Conteúdo com IA**: Utiliza a API Gemini para gerar ideias de posts, legendas, variações, hashtags e sugestões visuais com base no perfil do cliente e nos temas semanais.
- **Armazenamento de Dados**: Persistência de perfis de clientes e briefings gerados em um banco de dados SQLite.
- **Exportação de Briefing**: Geração de briefings em dois formatos:
    - **HTML**: Um arquivo HTML visualmente atraente, ideal para visualização rápida e compartilhamento digital.
    - **PDF**: Um documento PDF profissional, adequado para impressão e apresentação formal.
- **Flexibilidade de Saída**: A estrutura de saída permite a fácil adaptação para diferentes modelos de negócio, seja um briefing único ou relatórios mensais.

## Estrutura do Projeto
```
plataforma_automacao_ia_generativa/
├── mvp_concierge/
│   ├── backend_concierge_scripts/
│   │   ├── content_generator.py
│   │   ├── data_storage.py
│   │   ├── html_generator.py
│   │   ├── pdf_generator.py
│   │   ├── briefing_questions.md
│   │   └── __init__.py
│   ├── .env.example
│   ├── main.py
│   └── requirements.txt
├── README.md
└── ... (outros arquivos e diretórios)
```

## Configuração
Para configurar e executar o projeto, siga os passos abaixo:

1.  **Clone o Repositório**:
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd plataforma_automacao_ia_generativa/mvp_concierge
    ```

2.  **Crie e Ative um Ambiente Virtual (Recomendado)**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # No Windows
    # source venv/bin/activate  # No Linux/macOS
    ```

3.  **Instale as Dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente**:
    Crie um arquivo `.env` na pasta `mvp_concierge` (ao lado de `main.py`) e adicione sua chave de API do Google Gemini:
    ```
    GEMINI_API_KEY=SUA_CHAVE_DE_API_DO_GEMINI
    ```
    Você pode obter uma chave de API em [Google AI Studio](https://aistudio.google.com/app/apikey).

## Uso

### 1. Coleta de Informações do Cliente
As informações necessárias para gerar o briefing podem ser coletadas através de uma entrevista ou de um formulário (como o Google Forms). As perguntas essenciais estão detalhadas no arquivo `briefing_questions.md` localizado em `mvp_concierge/backend_concierge_scripts/briefing_questions.md`.

### 2. Executando o `main.py`
O arquivo `main.py` é o orquestrador principal. Ele receberá as informações do cliente, interagirá com o `content_generator.py` para gerar o conteúdo via IA, e então utilizará o `html_generator.py` e `pdf_generator.py` para criar os briefings nos formatos desejados.

Para executar o `main.py` (após preencher as informações do cliente e configurar o `.env`):

```bash
python main.py
```

**Nota**: Atualmente, o `main.py` precisa ser adaptado para receber os inputs das respostas da entrevista/formulário. Os dados serão armazenados automaticamente no banco de dados SQLite (`data/db.sqlite`).

## Modelo de Negócio
A estrutura atual da plataforma é flexível e pode suportar diferentes modelos de negócio:
- **Briefing Único**: O cliente paga por um briefing de conteúdo pontual (ex: 5 ideias de posts semanais).
- **Relatório Mensal/Recorrente**: A plataforma pode ser adaptada para gerar relatórios de conteúdo mensais ou recorrentes, oferecendo um serviço de assinatura.

## Próximos Passos e Melhorias Futuras
- **Integração de Input**: Desenvolver a interface ou método para o `main.py` receber as informações coletadas do cliente de forma estruturada.
- **Geração de Prompts para Imagens/Vídeos**: Implementar a funcionalidade para a IA gerar prompts descritivos para outras IAs de geração de imagem/vídeo.
- **Interface de Usuário (UI)**: Criar uma interface de usuário para facilitar a interação com a plataforma, a coleta de dados e a visualização dos briefings.
- **Autenticação e Gerenciamento de Clientes**: Adicionar funcionalidades de login, gerenciamento de múltiplos clientes e histórico de briefings.
- **Testes Abrangentes**: Implementar testes unitários e de integração para garantir a robustez da plataforma.