import streamlit as st

from frontend.utils import execute_query

@st.cache_data
def query_big_numbers():
    query = ('''
        SELECT distinct on (pollutant_code)
            pollutant_code,
            measurement_unit,
            state_code,
            avg_pollution
        FROM
            gold.mart_monitorar_big_numbers
        ORDER BY
            pollutant_code,
            avg_pollution DESC;
    ''')

    df = execute_query(query)

    return df

@st.cache_data
def query_media_mensal():
    query = '''
                SELECT
                    year_month,
                    state_code,
                    pollutant_code,
                    monthly_avg_pollution
                FROM
                    gold.mart_health_vs_air_quality
            '''

    df = execute_query(query)

    return df

@st.cache_data
def query_compare_pollutant_state():
    query = '''
                SELECT
                    year_month,
                    state_code,
                    pollutant_code,
                    monthly_avg_pollution
                FROM
                    gold.mart_health_vs_air_quality
            '''

    df = execute_query(query)

    return df

### ESTADO
@st.cache_data   
def query_poluicao_estado():
    
    query = (f'''
        SELECT
            pollutant_code,
            measurement_unit,
            state_code,
            avg_pollution
        FROM
            gold.mart_monitorar_big_numbers
        ORDER BY
            pollutant_code
    ''')

    df = execute_query(query)

    return df