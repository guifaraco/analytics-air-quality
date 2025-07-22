WITH fact_health_cases AS (
    SELECT
        patient_id,
        case_count
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
)

SELECT
    p.gender AS genero,
    p.age_group AS faixa_etaria,
    SUM(hc.case_count) AS numero_total_casos
FROM
    dim_patients AS p
JOIN
    fact_health_cases AS hc
    ON
    p.patient_id = hc.patient_id
WHERE
    p.gender != 'IGNORADO'
GROUP BY
    1, 2
ORDER BY
    p.age_group
