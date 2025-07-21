WITH fact_health_cases AS (
    SELECT
        *
    FROM
        {{ ref('fact_health_cases') }}
),

dim_risk_factors AS (
    SELECT
        *
    FROM
        {{ ref('dim_risk_factors') }}
)

SELECT
    SUM(CASE WHEN rf.is_puerpera='SIM' THEN 1 ELSE 0 END) AS total_cases_puerpera,
    SUM(CASE WHEN rf.has_chronic_cardiovascular_disease='SIM' THEN 1 ELSE 0 END) AS total_cases_cardiovascular,
    SUM(CASE WHEN rf.has_chronic_hematologic_disease='SIM' THEN 1 ELSE 0 END) AS total_cases_hematologic,
    SUM(CASE WHEN rf.has_down_syndrome='SIM' THEN 1 ELSE 0 END) AS total_cases_down_syndrome,
    SUM(CASE WHEN rf.has_chronic_liver_disease='SIM' THEN 1 ELSE 0 END) AS total_cases_liver_disease,
    SUM(CASE WHEN rf.has_asthma='SIM' THEN 1 ELSE 0 END) AS total_cases_asthma,
    SUM(CASE WHEN rf.has_diabetes='SIM' THEN 1 ELSE 0 END) AS total_cases_diabetes,
    SUM(CASE WHEN rf.has_chronic_neurological_disease='SIM' THEN 1 ELSE 0 END) AS total_cases_neurological,
    SUM(CASE WHEN rf.has_other_chronic_pneumopathy='SIM' THEN 1 ELSE 0 END) AS total_cases_pneumopathy,
    SUM(CASE WHEN rf.has_immunodeficiency='SIM' THEN 1 ELSE 0 END) AS total_cases_immunodeficiency,
    SUM(CASE WHEN rf.has_chronic_kidney_disease='SIM' THEN 1 ELSE 0 END) AS total_cases_kidney_disease,
    SUM(CASE WHEN rf.has_obesity='SIM' THEN 1 ELSE 0 END) AS total_cases_obesity,
    COUNT(hc.health_case_id) AS total_cases
FROM
    fact_health_cases AS hc
LEFT JOIN
    dim_risk_factors AS rf ON hc.risk_factors_id = rf.risk_factors_id
