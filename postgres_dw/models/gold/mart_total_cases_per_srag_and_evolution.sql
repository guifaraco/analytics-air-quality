WITH fact_health_cases AS (
    SELECT
        case_classification_id,
        case_count
    FROM
        {{ ref('fact_health_cases') }}
),

dim_case_classifications AS (
    SELECT
        case_classification_id,
        case_outcome,
        final_classification
    FROM
        {{ ref('dim_case_classifications') }}
)

SELECT
    cc.final_classification AS srag,
    cc.case_outcome AS evolucao,
    SUM(hc.case_count) AS numero_total_casos
FROM
    dim_case_classifications AS cc
INNER JOIN
    fact_health_cases AS hc
ON
    cc.case_classification_id = hc.case_classification_id
WHERE
    cc.final_classification != 'IGNORADO'
    AND cc.case_outcome != 'IGNORADO'
GROUP BY
    1, 2
ORDER BY
    1
