from utils.execute_query import execute_query

def query_big_numbers(filters={}):
    where_clauses = ["dp.pollutant_code IN ('MP10', 'NO2', 'SO2', 'O3', 'CO', 'MP2,5')"]

    if 'state_code' in filters:
        where_clauses.append(f"dl.state_code = '{filters['state_code']}'")
    if 'city_name' in filters:
        where_clauses.append(f"dl.city_name = '{filters['city_name']}'")

    where_clause = ' AND '.join(where_clauses)

    query = (f'''
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
            {where_clause}
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
    where_clauses = ["dp.pollutant_code in ('MP10', 'NO2', 'SO2', 'O3', 'CO')"]

    if 'state_code' in filters:
        where_clauses.append(f"dl.state_code = '{filters['state_code']}'")
    if 'city_name' in filters:
        where_clauses.append(f"dl.city_name = '{filters['city_name']}'")

    where_clause = ' AND '.join(where_clauses)
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