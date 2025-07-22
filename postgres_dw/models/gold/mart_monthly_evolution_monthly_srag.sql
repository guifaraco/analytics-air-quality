WITH fact_health_cases AS (
    SELECT
        first_symptoms_date_id,
        case_classification_id,
        case_count
    FROM
        {{ ref('fact_health_cases') }}
),

dim_date AS (
    SELECT
        date_id,
        month
    FROM
        {{ ref('dim_date') }}
),

dim_case_classifications AS (
    SELECT
        case_classification_id,
        final_classification,
        case_outcome
    FROM
        {{ ref('dim_case_classifications') }}
)

SELECT
  cc.final_classification,
  d.month,
  cc.case_outcome,
  SUM(hc.case_count)
FROM
    fact_health_cases AS hc
JOIN
    dim_date AS d ON hc.first_symptoms_date_id = d.date_id
JOIN
    dim_case_classifications AS cc ON hc.case_classification_id = cc.case_classification_id
WHERE
    cc.final_classification != 'IGNORADO'
GROUP BY
    cc.final_classification, d.month, case_outcome
ORDER BY
    d.month ASC
