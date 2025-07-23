import streamlit as st

from frontend.utils import execute_query


@st.cache_data
def query_casos_mensais_estado():
    '''
        Retorna os valores utilizados na primeira linha de big numbers.
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
                gold.mart_monthly_caes_by_state_classification
            '''

    return execute_query(query)