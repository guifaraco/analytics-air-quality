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
def query_media_mensal(states):
    clauses = ["dp.pollutant_code IN ('MP10', 'NO2', 'SO2', 'O3', 'CO', 'MP2,5')"]

    if states:
        clauses.append(f"dl.state_code IN ({' ,'.join(states)})")
    
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
def query_compare_pollutant_state(pollutant, states):
    clauses = [f"dp.pollutant_code = '{pollutant}'"]

    if states:
        clauses.append(f"dl.state_code IN ({' ,'.join(states)})")
    
    where_clause = ' AND '.join(clauses)
    
    query = (f'''
        select
            dd.month,
            dl.state_code,
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
            dd.month,
            dl.state_code
        order by
            dd.month;
    ''')

    df = execute_query(query)

    return df

### ESTADO
@st.cache_data   
def query_poluicao_estado(states, pollutant=''):
    where_clause = apply_filters(
        pollutant=pollutant,
        states=states
    )
    
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

def apply_filters(initial='1=1', pollutant='', states=[]):
    clauses = [initial]

    if states:
        clauses.append(f"state_code IN ({' ,'.join(states)})")
    if pollutant:
        clauses.append(f"pollutant_code = '{pollutant}'")

    return ' AND '.join(clauses)