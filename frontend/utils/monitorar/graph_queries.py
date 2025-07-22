import pandas as pd 

from frontend.utils import get_month_name ,execute_query

def query_big_numbers():
    query = ('''
        SELECT DISTINCT ON (dp.pollutant_code)
            dp.pollutant_code,
            dp.measurement_unit,
            dl.state_code,
            AVG(f.measurement_value) AS avg_pollution
        FROM
            gold.fact_air_quality_measurements f
        JOIN
            gold.dim_date dd ON f.date_id = dd.date_id
        JOIN
            gold.dim_pollutants dp ON f.pollutant_id = dp.pollutant_id
        JOIN
            gold.dim_locations dl ON f.location_id = dl.location_id
        WHERE
            dp.pollutant_code IN ('MP10', 'NO2', 'SO2', 'O3', 'CO', 'MP2,5')
        GROUP BY 
            dp.pollutant_code,
            dp.measurement_unit,
            dl.state_code
        ORDER BY
            dp.pollutant_code,
            AVG(f.measurement_value) DESC;
    ''')

    df = execute_query(query)

    return df

def query_media_mensal(filters={}):
    where_clause = apply_filters("dp.pollutant_code IN ('MP10', 'NO2', 'SO2', 'O3', 'CO', 'MP2,5')",filters)
    
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

    df['month_name'] = df['month'].astype(int).apply(get_month_name)

    return df

def query_map(filters={}):
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
    

def apply_filters(initial, filters):
    clauses = [initial]
    if 'state_code' in filters:
        clauses.append(f"dl.state_code = '{filters['state_code']}'")
    if 'pollutant_code' in filters:
        clauses.append(f"dp.pollutant_code = '{filters['pollutant_code']}'")

    return ' AND '.join(clauses)