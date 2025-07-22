import streamlit as st

from frontend.utils import get_month_name, execute_query

def query_big_numbers():
    first_query = ('''
        SELECT
            SUM(f.case_count) AS total_cases,
            ROUND(100.0 * SUM(f.case_count) FILTER (WHERE f.required_icu = 'SIM') / NULLIF(SUM(f.case_count), 0), 2) AS icu_percentage,
            ROUND(100.0 * SUM(f.case_count) FILTER (WHERE dc.case_outcome = 'OBITO') / NULLIF(SUM(f.case_count), 0), 2) AS death_percentage
        FROM
            gold.fact_health_cases f
        JOIN
            gold.dim_case_classifications dc ON f.case_classification_id = dc.case_classification_id
        '''
    )

    first_row = execute_query(first_query)

    second_query = ('''
        WITH classification_metrics AS (
            SELECT
                dc.final_classification,
                replace(replace(DC.FINAL_CLASSIFICATION, 'SRAG ', ''), 'POR ', '') as replaced,
                SUM(f.case_count) AS total_cases,
                ROUND(100.0 * SUM(f.case_count) FILTER (WHERE f.required_icu = 'SIM') / NULLIF(SUM(f.case_count), 0), 2) AS icu_percentage,
                ROUND(100.0 * SUM(f.case_count) FILTER (WHERE dc.case_outcome = 'OBITO') / NULLIF(SUM(f.case_count), 0), 2) AS death_percentage
            FROM
                gold.fact_health_cases f
            JOIN
                gold.dim_case_classifications dc ON f.case_classification_id = dc.case_classification_id
            WHERE
                dc.final_classification <> 'IGNORADO'
            GROUP BY
                dc.final_classification
        )
        SELECT
            (SELECT replaced FROM classification_metrics ORDER BY total_cases DESC LIMIT 1) AS srag_total_cases,
            (SELECT MAX(total_cases) FROM classification_metrics) AS max_total_cases,
            (SELECT replaced FROM classification_metrics ORDER BY icu_percentage DESC LIMIT 1) AS srag_icu_percentage,
            (SELECT MAX(icu_percentage) FROM classification_metrics) AS max_icu_percentage,
            (SELECT replaced FROM classification_metrics ORDER BY death_percentage DESC LIMIT 1) AS srag_death_percentage,
            (SELECT MAX(death_percentage) FROM classification_metrics) AS max_death_percentage;
        '''
    )

    second_row = execute_query(second_query)

    first_row = first_row.to_dict(orient='index')[0]
    second_row = second_row.to_dict(orient='index')[0]

    return first_row, second_row

def query_casos_mensais(filters={}):
    where_clause = apply_filters(filters, clauses=["dc.final_classification <> 'IGNORADO'", "dd.month <> 12"])

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

    df['month_name'] = df['month'].astype(int).apply(get_month_name)

    return df

def query_casos_map(filters={}):
    where_clause = apply_filters(filters, clauses=['1=1'])

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

def apply_filters(filters, clauses=[]):
    if 'state_code' in filters:
        clauses.append(f"dl.state_code = '{filters['state_code']}'")
    if 'final_classification' in filters:
        clauses.append(f"dc.final_classification = '{filters['final_classification']}'")

    return ' AND '.join(clauses)