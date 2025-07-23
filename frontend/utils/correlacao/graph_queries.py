import streamlit as st

from frontend.utils import execute_query

@st.cache_data
def query_big_numbers():
    '''
        Retorna os valores necessarios para os big numbers da pagina de correlacao agrupados por mes e poluente.
        Colunas retornadas:
            - month: mes referente as métricas
            - pollutant_code: sigla do poluente
            - total_cases: numero total de casos no mes
            - avg_pollution: média de poluição do poluente
            - hospitalization_percentage: percentual de pessoas hospitalizadas
            - icu_percentage: percentual de pessoas que foram pra UTI
            - death_percentage: percentual de obitos
    '''
    query = '''
            SELECT 
                *
            FROM
                gold.mart_datasus_monitorar_big_numbers
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