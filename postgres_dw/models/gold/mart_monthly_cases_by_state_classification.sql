    WITH fact_health_cases AS (
        SELECT
            case_classification_id,
            location_id,
            first_symptoms_date_id,
            case_count
        FROM
            {{ ref('fact_health_cases') }}
    ),

    dim_case_classifications AS (
        SELECT
            case_classification_id,
            final_classification
        FROM
            {{ ref('dim_case_classifications') }}
    ),

    dim_locations AS (
        SELECT
            location_id,
            state_code
        FROM
            {{ ref('dim_locations') }}
    ),

    dim_date AS (
        SELECT
            date_id,
            month
        FROM
            {{ ref('dim_date') }}
    )

    SELECT
        cc.final_classification,
        l.state_code,
        d.month,
        SUM(hc.case_count) AS total_cases
    FROM
        fact_health_cases hc
    JOIN
        dim_case_classifications cc ON hc.case_classification_id = cc.case_classification_id
    JOIN
        dim_locations l ON hc.location_id = l.location_id
    JOIN
        dim_date d ON hc.first_symptoms_date_id = d.date_id
    WHERE
        final_classification != 'IGNORADO'
    GROUP BY
        cc.final_classification,
        l.state_code,
        d.month
    ORDER BY
        numero_total_casos DESC
