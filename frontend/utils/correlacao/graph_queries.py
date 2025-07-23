import streamlit as st

from frontend.utils import execute_query


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

@st.cache_data
def query_correlacao_poluicao_casos():
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
                    ha.year_month AS ano_mes,
                    ha.pollutant_code AS poluente,
                    ha.state_code AS uf,
                    ha.total_health_cases AS numero_total_casos,
                    ha.monthly_avg_pollution AS media_poluicao
            FROM 
                    gold.mart_health_vs_air_quality AS ha
            GROUP BY
                    1, 2, 3, 4, 5
    '''

    return execute_query(query)