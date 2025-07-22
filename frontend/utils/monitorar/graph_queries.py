import streamlit as st
import pandas as pd 

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
def query_media_mensal(filters={}):
    clauses = ["dp.pollutant_code IN ('MP10', 'NO2', 'SO2', 'O3', 'CO', 'MP2,5')"]

    if 'state_code' in filters:
        clauses.append(f"dl.state_code = '{filters['state_code']}'")
    if 'pollutant_code' in filters:
        clauses.append(f"dp.pollutant_code = '{filters['pollutant_code']}'")

    where_clause = ' AND '.join(clauses)
    
    query = (f'''
        select
            dd.month,
            dp.pollutant_code,
            avg(f.measurement_value) as monthly_avg_pollution
        from
            gold.fact_air_quality_measurements f 
        join
            gold.dim_date dd on f.date_id = dd.date_id
        join
            gold.dim_pollutants dp on f.pollutant_id = dp.pollutant_id
        join
            gold.dim_locations dl on f.location_id = dl.location_id
        where
            {where_clause}
        group by 
            dp.pollutant_code,
            dd.month
        order by
            dd.month;
    ''')

    df = execute_query(query)

    return df

@st.cache_data
def query_map():
    query = (f'''
        select
            state_code,
            avg(avg_pollution_value) as avg_pollution
        from
            gold.mart_map dl
        group by
            state_code 
    ''')

    df = execute_query(query)

    br_states = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    # Cria um DataFrame "base" que servirá como a lista completa
    df_todos_estados = pd.DataFrame(br_states, columns=['state_code'])

    # Junta o DataFrame completo com os dados da query
    # O 'how="left"' garante que todos os estados da lista completa sejam mantidos.
    # Para os estados que não estavam no resultado da query, o valor de 'avg_pollution' será NaN (nulo).
    final_df = pd.merge(df_todos_estados, df, on='state_code', how='left')

    # Todos os campos de média de poluição Nulos serão tratados como 0 para que apareça no mapa
    final_df['avg_pollution'] = final_df['avg_pollution'].fillna(0)

    return final_df

@st.cache_data   
def query_poluicao_estado(filters={}):
    where_clause = apply_filters("1=1",filters)
    
    query = (f'''
        SELECT
            pollutant_code,
            measurement_unit,
            state_code,
            avg_pollution
        FROM
            gold.mart_monitorar_big_numbers
        WHERE
            {where_clause}
        ORDER BY
            pollutant_code
    ''')

    df = execute_query(query)

    return df

def apply_filters(initial, filters):
    clauses = [initial]
    if 'state_code' in filters:
        clauses.append(f"state_code = '{filters['state_code']}'")
    if 'pollutant_code' in filters:
        clauses.append(f"pollutant_code = '{filters['pollutant_code']}'")

    return ' AND '.join(clauses)