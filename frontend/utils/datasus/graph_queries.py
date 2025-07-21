from utils.execute_query import execute_query

def query_big_numbers(filters={}):
    where_clause = apply_filters("dc.final_classification <> 'IGNORADO'", filters)

    query = (f'''
        WITH cases_by_classification_age AS (
            SELECT
                dc.final_classification,
                dp.age_group,
                SUM(f.case_count) AS total_cases,
                SUM(f.case_count) FILTER (WHERE dc.case_outcome = 'OBITO') AS total_deaths
            FROM
                gold.fact_health_cases f
            JOIN
                gold.dim_case_classifications dc ON f.case_classification_id = dc.case_classification_id
            JOIN
                gold.dim_patients dp ON f.patient_id = dp.patient_id
            JOIN
                gold.dim_locations dl ON f.location_id = dl.location_id
            WHERE
                {where_clause}
            GROUP BY
                dc.final_classification,
                dp.age_group
        ),
        ranked_by_cases AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY final_classification 
                    ORDER BY total_cases DESC
                ) AS rn
            FROM cases_by_classification_age
        )
        SELECT
            final_classification,
            age_group,
            total_cases,
            total_deaths,
            ROUND(
                100.0 * total_deaths / NULLIF(total_cases, 0),
                2
            ) AS death_percentage
        FROM
            ranked_by_cases
        WHERE
            rn = 1
        ORDER BY
            death_percentage DESC;
        '''
    )

    df = execute_query(query)

    return df

def query_casos_mensais(filters={}):
    where_clause = apply_filters("dc.final_classification <> 'IGNORADO'", filters)

    query = (f'''
        select
            dd.month,
            dc.final_classification,
            SUM(f.case_count) AS total_cases
        from
            gold.fact_health_cases f 
        join
            gold.dim_date dd on f.first_symptoms_date_id = dd.date_id
        join
            gold.dim_case_classifications dc ON f.case_classification_id = dc.case_classification_id
        join
            gold.dim_locations dl on f.location_id = dl.location_id
        where
            {where_clause}
        group by 
            dc.final_classification,
            dd.month
        order by
            dd.month;
    ''')

    df = execute_query(query)

    return df

def query_casos_map(filters={}):
    where_clause = apply_filters("1=1", filters)

    query = (f'''
        SELECT
            dms.city_name,
            ARRAY[
                AVG(dms.longitude)::double precision,
                AVG(dms.latitude)::double precision
            ] AS coordinates,
            f.total_cases
        FROM
            gold.dim_monitoring_stations dms
        join (
            SELECT 
                f.location_id,
                SUM(f.case_count) AS total_cases
            FROM 
                gold.fact_health_cases f
            join
                gold.dim_locations dl on f.location_id = dl.location_id
            join
                gold.dim_case_classifications dc on f.case_classification_id = dc.case_classification_id
            WHERE
                {where_clause}
            GROUP BY 
                f.location_id
        ) f on f.location_id = dms.location_id
        GROUP BY
            dms.city_name,
            f.total_cases
    ''')

    df = execute_query(query)

    return df

def apply_filters(initial, filters):
    clauses = [initial]
    if 'state_code' in filters:
        clauses.append(f"dl.state_code = '{filters['state_code']}'")
    if 'final_classification' in filters:
        clauses.append(f"dc.final_classification = '{filters['final_classification']}'")
    if 'city_name' in filters:
        clauses.append(f"dl.city_name = '{filters['city_name']}'")

    return ' AND '.join(clauses)