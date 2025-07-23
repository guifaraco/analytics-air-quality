WITH fact_health_cases AS (
    SELECT
        patient_id,
        case_count,
        case_classification_id
    FROM
        {{ ref('fact_health_cases') }}
),

dim_patients AS (
    SELECT
        patient_id,
        gender,
        age_group
    FROM
        {{ ref('dim_patients') }}
),

dim_case_classifications AS (
    SELECT
        case_classification_id,
        final_classification
    FROM
        {{ ref('dim_case_classifications') }}
)

SELECT
    p.gender AS genero,
    p.age_group AS faixa_etaria,
    cc.final_classification,
    SUM(hc.case_count) AS numero_total_casos
FROM
    dim_patients AS p
JOIN
    fact_health_cases AS hc
    ON
    p.patient_id = hc.patient_id
JOIN
    dim_case_classifications AS cc
    ON
    cc.case_classification_id = hc.case_classification_id
WHERE
    p.gender != 'IGNORADO'
    AND final_classification != 'IGNORADO'
GROUP BY
    1, 2, 3
ORDER BY
    p.age_group
