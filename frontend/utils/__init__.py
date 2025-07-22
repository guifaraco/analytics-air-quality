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

def get_month_name(df, coluna_mes='month'):
    """
    Converte uma coluna numérica de meses (1-12) para nomes em português.
    
    Args:
        df: DataFrame pandas.
        coluna_mes: Nome da coluna com os números dos meses.
    
    Returns:
        DataFrame com a coluna modificada e ordenada corretamente.
    """
    # Mapeamento número -> nome do mês
    meses_pt = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro'
    }
    
    # Converte os números para nomes
    df[coluna_mes] = df[coluna_mes].map(meses_pt)
    
    # Garante a ordem cronológica
    ordem_meses = list(meses_pt.values())
    df[coluna_mes] = pd.Categorical(
        df[coluna_mes],
        categories=ordem_meses,
        ordered=True
    )
    
    return df.sort_values(coluna_mes)

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