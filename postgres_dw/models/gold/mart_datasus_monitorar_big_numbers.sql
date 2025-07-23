-- CTE para agregar as métricas de daúde por mês.
WITH health_metrics_monthly AS (
    SELECT
        d.month,
        
        -- Contagens brutas de eventos
        SUM(f.case_count) AS total_cases,
        SUM(
            CASE 
            WHEN f.was_hospitalized = 'SIM' THEN 1
            WHEN (f.was_hospitalized != 'SIM' AND f.required_icu = 'SIM') THEN 1 
            ELSE 0 END
        ) AS total_hospitalizations,
        SUM(CASE WHEN f.required_icu = 'SIM' THEN 1 ELSE 0 END) AS total_icu_cases,
        SUM(CASE WHEN cc.case_outcome = 'OBITO' THEN 1 ELSE 0 END) AS total_deaths
        
    FROM
        {{ ref('fact_health_cases') }} AS f
    JOIN
        {{ ref('dim_date') }} AS d ON f.first_symptoms_date_id = d.date_id
    JOIN
        {{ ref('dim_case_classifications') }} AS cc ON f.case_classification_id = cc.case_classification_id
    WHERE
        cc.final_classification != 'IGNORADO'
        AND cc.case_outcome != 'IGNORADO'
        AND (f.was_hospitalized != 'IGNORADO' OR f.required_icu != 'IGNORADO') 
    GROUP BY
        d.month -- Agrupa por ano/mês
),

-- CTE para agregar as métricas de poluição por mês e por poluente.
pollution_metrics_monthly AS (
    SELECT
        d.month,
        p.pollutant_code,
        AVG(f.measurement_value) AS avg_pollution
    FROM
        {{ ref('fact_air_quality_measurements') }} AS f
    JOIN
        {{ ref('dim_date') }} AS d ON f.date_id = d.date_id
    JOIN
        {{ ref('dim_pollutants') }} AS p ON f.pollutant_id = p.pollutant_id
    WHERE
        p.pollutant_code IN ('MP2,5', 'SO2', 'NO2', 'MP10', 'CO', 'O3')
    GROUP BY
        d.month, p.pollutant_code -- Agrupa por ano/mês e por poluente
)

-- Juntamos as métricas de saúde e poluição
SELECT
    p.month,
    p.pollutant_code,
    
    -- Métricas Finais
    COALESCE(h.total_cases, 0) AS total_cases,
    p.avg_pollution,
    
    -- Taxas em Porcentagem (KPIs)
    ROUND((COALESCE(h.total_hospitalizations, 0) * 100.0) / NULLIF(h.total_cases, 0), 2) AS hospitalization_percentage,
    ROUND((COALESCE(h.total_icu_cases, 0) * 100.0) / NULLIF(h.total_cases, 0), 2) AS icu_percentage,
    ROUND((COALESCE(h.total_deaths, 0) * 100.0) / NULLIF(h.total_cases, 0), 2) AS death_percentage

FROM
    pollution_metrics_monthly AS p
JOIN
    health_metrics_monthly AS h ON p.month = h.month
ORDER BY
    p.month,
    p.pollutant_code