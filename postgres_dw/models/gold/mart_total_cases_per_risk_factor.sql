-- CTE para unir os fatos com a dimensão de fatores de risco apenas uma vez.
WITH joined_data AS (
    SELECT
        rf.is_puerpera,
        rf.has_chronic_cardiovascular_disease,
        rf.has_chronic_hematologic_disease,
        rf.has_down_syndrome,
        rf.has_chronic_liver_disease,
        rf.has_asthma,
        rf.has_diabetes,
        rf.has_chronic_neurological_disease,
        rf.has_other_chronic_pneumopathy,
        rf.has_immunodeficiency,
        rf.has_chronic_kidney_disease,
        rf.has_obesity,
        -- E a chave de UTI da tabela de fatos
        hc.required_icu
    FROM
        {{ ref('fact_health_cases') }} AS hc
    LEFT JOIN
        {{ ref('dim_risk_factors') }} AS rf ON hc.risk_factors_id = rf.risk_factors_id
)

-- Desempilhamos cada coluna de fator de risco usando UNION ALL

SELECT
    'Puérpera' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE is_puerpera = 'SIM'

UNION ALL

SELECT
    'Doença Cardiovascular' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_cardiovascular_disease = 'SIM'

UNION ALL

SELECT
    'Doença Hematológica' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_hematologic_disease = 'SIM'

UNION ALL

SELECT
    'Síndrome de Down' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_down_syndrome = 'SIM'

UNION ALL

SELECT
    'Doença Hepática' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_liver_disease = 'SIM'

UNION ALL

SELECT
    'Asma' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_asthma = 'SIM'

UNION ALL

SELECT
    'Diabetes' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_diabetes = 'SIM'

UNION ALL

SELECT
    'Doença Neurológica' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_neurological_disease = 'SIM'

UNION ALL

SELECT
    'Outra Pneumopatia' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_other_chronic_pneumopathy = 'SIM'

UNION ALL

SELECT
    'Imunodeficiência' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_immunodeficiency = 'SIM'

UNION ALL

SELECT
    'Doença Renal' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_kidney_disease = 'SIM'

UNION ALL

SELECT
    'Obesidade' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_obesity = 'SIM'

ORDER BY
    total_icu_cases DESC
