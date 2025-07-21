WITH fact_health_cases AS (
    SELECT
        *
    FROM
        {{ ref('fact_health_cases') }}
),

dim_symptoms AS (
    SELECT
        *
    FROM
        {{ ref('dim_symptoms') }}
)

SELECT
    SUM(CASE WHEN s.had_fever='SIM' THEN 1 ELSE 0 END) AS total_cases_had_fever,
    SUM(CASE WHEN s.had_fever='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_fever,

    SUM(CASE WHEN s.had_cough='SIM' THEN 1 ELSE 0 END) AS total_cases_had_cough,
    SUM(CASE WHEN s.had_cough='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_cough,

    SUM(CASE WHEN s.had_sore_throat='SIM' THEN 1 ELSE 0 END) AS total_cases_had_sore_throat,
    SUM(CASE WHEN s.had_sore_throat='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_sore_throat,

    SUM(CASE WHEN s.had_dyspnea='SIM' THEN 1 ELSE 0 END) AS total_cases_had_dyspnea,
    SUM(CASE WHEN s.had_dyspnea='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_dyspnea,

    SUM(CASE WHEN s.had_respiratory_distress='SIM' THEN 1 ELSE 0 END) AS total_cases_had_respiratory_distress,
    SUM(CASE WHEN s.had_respiratory_distress='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_respiratory_distress,

    SUM(CASE WHEN s.had_low_saturation='SIM' THEN 1 ELSE 0 END) AS total_cases_had_low_saturation,
    SUM(CASE WHEN s.had_low_saturation='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_low_saturation,

    SUM(CASE WHEN s.had_diarrhea='SIM' THEN 1 ELSE 0 END) AS total_cases_had_diarrhea,
    SUM(CASE WHEN s.had_diarrhea='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_diarrhea,

    SUM(CASE WHEN s.had_vomiting='SIM' THEN 1 ELSE 0 END) AS total_cases_had_vomiting,
    SUM(CASE WHEN s.had_vomiting='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_vomiting,

    SUM(CASE WHEN s.had_fatigue='SIM' THEN 1 ELSE 0 END) AS total_cases_had_fatigue,
    SUM(CASE WHEN s.had_fatigue='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_fatigue,

    SUM(CASE WHEN s.had_loss_of_smell='SIM' THEN 1 ELSE 0 END) AS total_cases_had_loss_of_smell,
    SUM(CASE WHEN s.had_loss_of_smell='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_loss_of_smell,

    SUM(CASE WHEN s.had_loss_of_taste='SIM' THEN 1 ELSE 0 END) AS total_cases_had_loss_of_taste,
    SUM(CASE WHEN s.had_loss_of_taste='SIM' AND hc.required_icu='SIM' THEN 1 ELSE 0 END) AS icu_cases_had_loss_of_taste,

    COUNT(hc.health_case_id) AS total_cases,
    SUM(CASE WHEN hc.required_icu='SIM' THEN 1 ELSE 0 END) AS total_icu_cases
FROM
    fact_health_cases AS hc
LEFT JOIN
    dim_symptoms AS s ON hc.symptoms_id = s.symptoms_id
