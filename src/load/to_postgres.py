import pandas as pd
from io import StringIO

def load_to_postgres(df: pd.DataFrame, conn, schema: str, table_name: str):
    """
    Carrega um DataFrame para uma tabela no PostgreSQL.
    A tabela será criada ou substituída.
    """
    if df.empty:
        print("DataFrame está vazio. Nenhuma carga será realizada.")
        return

    full_table_name = f"{schema}.{table_name}"
    print(f"Iniciando carga para a tabela '{full_table_name}'...")

    # Cria um buffer de texto na memória para "fingir" que o DataFrame é um arquivo CSV
    buffer = StringIO()
    # Converte o DataFrame para um formato CSV no buffer, sem índice e sem cabeçalho
    # Usamos tab como separador para evitar problemas com vírgulas nos dados
    df.to_csv(buffer, index=False, header=False, sep='\t')
    # Volta para o início do buffer para a leitura
    buffer.seek(0)
    
    with conn.cursor() as cur:
        # Garante que o schema exista
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
        
        # Apaga a tabela se ela já existir
        cur.execute(f"DROP TABLE IF EXISTS {full_table_name};")
        
        # Cria a tabela com as colunas e tipos de dados do DataFrame
        colunas_sql = ", ".join([f'"{col}" TEXT' for col in df.columns])
        cur.execute(f"CREATE TABLE {full_table_name} ({colunas_sql});")
        print(f"Tabela '{full_table_name}' criada com sucesso.")

        # Insere os dados na tabela
        print("Inserindo dados...")
        with cur.copy(f"COPY {full_table_name} FROM STDIN WITH (FORMAT CSV, DELIMITER E'\\t')") as copy:
            copy.write(buffer.read())
            
    print(f"{len(df)} registros carregados com sucesso em '{full_table_name}'.")
