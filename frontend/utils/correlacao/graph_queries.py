import streamlit as st

from frontend.utils import execute_query

def query_big_numbers():
    print()

def query_total_casos():
    '''
        Retorna o total de casos por mes.
        Colunas retornadas:
            - total_cases: numero total de casos no mes
            - month: mes que ocorreu o caso
    '''

    query = '''
            SELECT 
                month,
                SUM(sum)
            FROM
                gold.mart_total_cases_monthly
            WHERE
                month <> 12
            GROUP BY
                month
            ORDER BY
                month
            '''

    return execute_query(query)

def query_taxa_mortalidade():
    '''
        Retorna os valores de taxa de mortalidade agrupados por mes.
        Colunas retornadas:
            - final_classification: nome da srag
            - state_code: sigla do estado do caso da srag
            - month: mes que ocorreu o caso
            - total_cases: numero total de casos da srag
    '''

    query = '''
            SELECT 
                *
            FROM
                gold.mart_monthly_cases_by_state_classification
            '''

    return execute_query(query)

@st.cache_data
def query_casos_mensais_estado():
    '''
        Retorna os valores utilizados no gráfico de correlação entre as SRAGs.
        Colunas retornadas:
            - final_classification: nome da srag
            - state_code: sigla do estado do caso da srag
            - month: mes que ocorreu o caso
            - total_cases: numero total de casos da srag
    '''

    query = '''
            SELECT 
                *
            FROM
                gold.mart_monthly_cases_by_state_classification
            '''

    return execute_query(query)