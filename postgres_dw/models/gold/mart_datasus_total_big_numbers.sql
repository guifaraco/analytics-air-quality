WITH classification_metrics AS (
    SELECT
        cc.final_classification,

        SUM(f.case_count) AS total_cases,

        -- Calcula a porcentagem e arredonda a pocentagem para duas casas decimais
        ROUND(
            100.0 * SUM(CASE WHEN f.required_icu = 'SIM' THEN 1 ELSE 0 END) /
            NULLIF(SUM(f.case_count), 0),
        2) AS icu_percentage,

        ROUND(
            100.0 * SUM(CASE WHEN cc.case_outcome = 'OBITO' THEN 1 ELSE 0 END) /
            NULLIF(SUM(f.case_count), 0),
        2) AS death_percentage

    FROM
        {{ ref('fact_health_cases') }} AS f
    JOIN
        {{ ref('dim_case_classifications') }} AS cc ON f.case_classification_id = cc.case_classification_id
    WHERE
        cc.final_classification != 'IGNORADO'
        AND cc.case_outcome != 'IGNORADO'
    GROUP BY
        cc.final_classification
)

SELECT * FROM classification_metrics ORDER BY total_cases DESC
