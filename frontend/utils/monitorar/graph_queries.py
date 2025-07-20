from utils.execute_query import execute_query

import streamlit as st

def query_media_mensal(filters={}):
    query = ('''
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
            dp.pollutant_code in ('PM10', 'NO2', 'SO2', 'O3', 'CO')
        '''
    )
    if filters:
        query += ' AND '
        query = apply_filters(query, filters)

    query += ('''
        group by 
            dp.pollutant_code,
            dd.month
        order by
            dd.month;
    ''')

    st.write(query)
    print(query)

    df = execute_query(query)

    return df

def apply_filters(query, filters):
    filters = [f"{column} = '{value}'" for column, value in filters.items()]

    if filters:
        query += f" {' AND '.join(filters)}"
    
    return query