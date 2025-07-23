-- CTE para unir os fatos com a dimensão de sintomas apenas uma vez.
WITH joined_data AS (
    SELECT
        s.had_fever,
        s.had_cough,
        s.had_sore_throat,
        s.had_dyspnea,
        s.had_respiratory_distress,
        s.had_low_saturation,
        s.had_diarrhea,
        s.had_vomiting,
        s.had_fatigue,
        s.had_loss_of_smell,
        s.had_loss_of_taste,
        hc.required_icu,
        hc.case_classification_id,
        cc.final_classification
    FROM
        {{ ref('fact_health_cases') }} AS hc
    LEFT JOIN
        {{ ref('dim_symptoms') }} AS s ON hc.symptoms_id = s.symptoms_id
    LEFT JOIN
        {{ ref('dim_case_classifications') }} as cc ON hc.case_classification_id = cc.case_classification_id
)

-- Desempilhamos cada coluna de sintoma usando UNION ALL
SELECT
    final_classification,
    'Febre' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_fever = 'SIM' -- Filtra apenas os casos que tiveram este sintoma
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Tosse' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_cough = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Dor de Garganta' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_sore_throat = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Dispneia' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_dyspnea = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Desconforto Respiratório' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_respiratory_distress = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Saturação < 95%' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_low_saturation = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Diarreia' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_diarrhea = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Vômito' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_vomiting = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Fadiga' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_fatigue = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Perda de Olfato' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_loss_of_smell = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

UNION ALL

SELECT
    final_classification,
    'Perda de Paladar' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_loss_of_taste = 'SIM'
    AND final_classification != 'IGNORADO'
GROUP BY final_classification

ORDER BY
    total_icu_cases DESC
