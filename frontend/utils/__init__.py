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

def get_month_name(number):
    meses = [
        "",          # índice 0 (vazio, para que 1 = Janeiro)
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    return meses[number]

def get_states_list():
    states_df = execute_query('''
        SELECT DISTINCT
            state_code 
        FROM 
            gold.dim_locations 
        ORDER BY 
            state_code'''
    )
    
    states_list= list(states_df['state_code'])

    return states_list