-- CTE base para calcular as métricas para CADA classificação de doença.
WITH classification_metrics AS (
    SELECT
        cc.final_classification,

        SUM(f.case_count) AS total_cases,

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
),

-- CTE para rankear os resultados de acordo com cada métrica.
ranked_classifications AS (
    SELECT
        *,
        -- Rank 1 para a classificação com o maior número total de casos
        ROW_NUMBER() OVER (ORDER BY total_cases DESC) as rank_total_cases,

        -- Rank 1 para a classificação com a maior porcentagem de UTI
        ROW_NUMBER() OVER (ORDER BY icu_percentage DESC) as rank_icu,

        -- Rank 1 para a classificação com a maior porcentagem de óbito
        ROW_NUMBER() OVER (ORDER BY death_percentage DESC) as rank_death
    FROM
        classification_metrics
)

SELECT
    -- Pega o NOME da classificação onde o rank de casos totais é 1
    MAX(CASE WHEN rank_total_cases = 1 THEN final_classification END) AS top_classification_by_total_cases,
    -- Pega o VALOR máximo de casos totais
    MAX(total_cases) AS max_total_cases,

    -- Repete o padrão para a porcentagem de UTI
    MAX(CASE WHEN rank_icu = 1 THEN final_classification END) AS top_classification_by_icu_rate,
    MAX(icu_percentage) AS max_icu_rate,

    -- Repete o padrão para a porcentagem de óbito
    MAX(CASE WHEN rank_death = 1 THEN final_classification END) AS top_classification_by_death_rate,
    MAX(death_percentage) AS max_death_rate
FROM
    ranked_classifications
