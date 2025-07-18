import pandas as pd

from src.main import get_db_connection

def execute_query(query, params=None):
    """
    Executa uma query SELECT e retorna os resultados como lista de dicionários.
    
    :param conn: conexão do psycopg
    :param query: string com a query SQL
    :param params: parâmetros opcionais para a query (tuple ou list)
    :return: lista de dicionários, onde cada dicionário representa uma linha
    """

    conn = get_db_connection()
    
    with conn.cursor() as cur:
        cur.execute(query, params)
        # Pega os nomes das colunas
        colnames = [desc[0] for desc in cur.description]
        # Pega todas as linhas
        rows = cur.fetchall()
    
    # Cria DataFrame com colunas e dados
    df = pd.DataFrame(rows, columns=colnames)
    return df

def select(view, cols, schema='gold', filters={}, distinct=False):
    query = "SELECT "
    if distinct:
        query += "DISTINCT "
    query += f"{', '.join(cols)} FROM {schema}.{view} "

    filters = [f"{column} = {value}" for column, value in filters.items()]

    if filters:
        query += f"WHERE {' AND '.join(filters)}"
    
    df = execute_query(query)
    return df