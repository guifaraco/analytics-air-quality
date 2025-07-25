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
        hc.required_icu,
        hc.case_classification_id,
        cc.final_classification
    FROM
        {{ ref('fact_health_cases') }} AS hc
    LEFT JOIN
        {{ ref('dim_risk_factors') }} AS rf ON hc.risk_factors_id = rf.risk_factors_id
    LEFT JOIN
        {{ ref('dim_case_classifications') }} as cc ON hc.case_classification_id = cc.case_classification_id
)

-- Desempilhamos cada coluna de fator de risco usando UNION ALL
SELECT
    final_classification,
    'Puérpera' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE is_puerpera = 'SIM'
        AND final_classification != 'IGNORADO'
GROUP BY final_classification


UNION ALL

SELECT
    final_classification,
    'Doença Cardiovascular' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_cardiovascular_disease = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Doença Hematológica' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_hematologic_disease = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Síndrome de Down' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_down_syndrome = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Doença Hepática' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_liver_disease = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Asma' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_asthma = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Diabetes' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_diabetes = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Doença Neurológica' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_neurological_disease = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Outra Pneumopatia' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_other_chronic_pneumopathy = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Imunodeficiência' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_immunodeficiency = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Doença Renal' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_chronic_kidney_disease = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
UNION ALL

SELECT
    final_classification,
    'Obesidade' AS risk_factor_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM'THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM'THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE has_obesity = 'SIM'
AND final_classification != 'IGNORADO'
GROUP BY final_classification
ORDER BY
    total_icu_cases DESC
