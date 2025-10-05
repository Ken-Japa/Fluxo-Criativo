import sqlite3
import json
from datetime import datetime

DATABASE_PATH = 'data/db.sqlite'

def init_db():
    """
    Conecta-se ao banco de dados SQLite e cria as tabelas 'client_briefs' e 'client_profiles'
    se elas não existirem.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Tabela client_briefs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_briefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            subniche TEXT,
            brief_data TEXT,
            generated_content TEXT,
            prompt_used TEXT,
            tokens_consumed INTEGER,
            api_cost_usd REAL,
            delivery_date TEXT,
            feedback_summary TEXT
        )
    """)

    # Tabela client_profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT UNIQUE NOT NULL,
            contact_info TEXT,
            public_target TEXT,
            tone_of_voice TEXT,
            niche_examples TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Banco de dados inicializado e tabelas criadas (se não existiam).")

def insert_brief(client_name: str, subniche: str, brief_data: dict,
                 generated_content: dict, prompt_used: str, tokens_consumed: int,
                 api_cost_usd: float, delivery_date: str = None):
    """
    Insere um novo registro de briefing e conteúdo gerado no banco de dados.

    Args:
        client_name (str): Nome do cliente.
        subniche (str): Subnicho do cliente.
        brief_data (dict): Dados do briefing (será armazenado como JSON string).
        generated_content (dict): Conteúdo gerado (será armazenado como JSON string).
        prompt_used (str): O prompt exato usado para gerar o conteúdo.
        tokens_consumed (int): Número de tokens consumidos na geração.
        api_cost_usd (float): Custo da API em USD.
        delivery_date (str, optional): Data de entrega no formato YYYY-MM-DD.
                                       Padrão para a data atual se não fornecido.
    """
    if delivery_date is None:
        delivery_date = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO client_briefs (client_name, subniche, brief_data, generated_content,
                                   prompt_used, tokens_consumed, api_cost_usd, delivery_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (client_name, subniche, json.dumps(brief_data), json.dumps(generated_content),
          prompt_used, tokens_consumed, api_cost_usd, delivery_date))
    conn.commit()
    conn.close()
    print(f"Briefing para '{client_name}' inserido com sucesso.")

def get_briefs_by_client(client_name: str) -> list:
    """
    Retorna todos os briefings e conteúdos gerados para um cliente específico.

    Args:
        client_name (str): Nome do cliente.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um briefing.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client_briefs WHERE client_name = ?", (client_name,))
    rows = cursor.fetchall()
    conn.close()

    briefs = []
    for row in rows:
        briefs.append({
            "id": row[0],
            "client_name": row[1],
            "subniche": row[2],
            "brief_data": json.loads(row[3]),
            "generated_content": json.loads(row[4]),
            "prompt_used": row[5],
            "tokens_consumed": row[6],
            "api_cost_usd": row[7],
            "delivery_date": row[8],
            "feedback_summary": row[9]
        })
    return briefs

def insert_client_profile(client_name: str, contact_info: str, public_target: str,
                          tone_of_voice: str, niche_examples: list, status: str = 'active'):
    """
    Insere ou atualiza um perfil de cliente no banco de dados.
    Se o cliente já existir, o perfil será atualizado.

    Args:
        client_name (str): Nome único do cliente.
        contact_info (str): Informações de contato do cliente.
        public_target (str): Público-alvo do cliente.
        tone_of_voice (str): Tom de voz preferido do cliente.
        niche_examples (list): Exemplos de nicho (será armazenado como JSON string).
        status (str, optional): Status do cliente (ex: 'active', 'inactive', 'trial').
                                Padrão é 'active'.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO client_profiles (client_name, contact_info, public_target,
                                               tone_of_voice, niche_examples, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (client_name, contact_info, public_target, tone_of_voice,
          json.dumps(niche_examples), status))
    conn.commit()
    conn.close()
    print(f"Perfil do cliente '{client_name}' inserido/atualizado com sucesso.")

def get_client_profile(client_name: str) -> dict:
    """
    Retorna o perfil de um cliente específico.

    Args:
        client_name (str): Nome do cliente.

    Returns:
        dict: Um dicionário representando o perfil do cliente, ou None se não encontrado.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client_profiles WHERE client_name = ?", (client_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "client_name": row[1],
            "contact_info": row[2],
            "public_target": row[3],
            "tone_of_voice": row[4],
            "niche_examples": json.loads(row[5]),
            "status": row[6]
        }
    return None

def update_brief_feedback(brief_id: int, feedback_summary: str):
    """
    Atualiza um registro de briefing com um resumo do feedback do cliente.

    Args:
        brief_id (int): O ID do briefing a ser atualizado.
        feedback_summary (str): O resumo do feedback do cliente.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE client_briefs
        SET feedback_summary = ?
        WHERE id = ?
    """, (feedback_summary, brief_id))
    conn.commit()
    conn.close()
    print(f"Feedback para o briefing ID {brief_id} atualizado com sucesso.")