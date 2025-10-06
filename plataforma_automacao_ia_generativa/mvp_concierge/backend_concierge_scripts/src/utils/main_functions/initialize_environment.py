import os
from src.data_storage import init_db
from src.config import BASE_DIR

def initialize_environment():
    """
    Inicializa o banco de dados e cria o diretório de saída para os arquivos gerados.
    """
    print("Inicializando o banco de dados...")
    init_db()
    print("Banco de dados pronto.")

    output_dir = os.path.join(BASE_DIR, "output_files")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Diretório de saída para arquivos gerados: {output_dir}")
    return output_dir