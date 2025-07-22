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
        hc.required_icu
    FROM
        {{ ref('fact_health_cases') }} AS hc
    LEFT JOIN
        {{ ref('dim_symptoms') }} AS s ON hc.symptoms_id = s.symptoms_id
)

-- Desempilhamos cada coluna de sintoma usando UNION ALL

-- Febre
SELECT
    'Febre' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_fever = 'SIM' -- Filtra apenas os casos que tiveram este sintoma

UNION ALL

-- Tosse
SELECT
    'Tosse' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_cough = 'SIM'

UNION ALL

-- Dor de Garganta
SELECT
    'Dor de Garganta' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_sore_throat = 'SIM'

UNION ALL

-- Dispneia
SELECT
    'Dispneia' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_dyspnea = 'SIM'

UNION ALL

-- Desconforto Respiratório
SELECT
    'Desconforto Respiratório' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_respiratory_distress = 'SIM'

UNION ALL

-- Saturação Baixa
SELECT
    'Saturação < 95%' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_low_saturation = 'SIM'

UNION ALL

-- Diarreia
SELECT
    'Diarreia' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_diarrhea = 'SIM'

UNION ALL

-- Vômito
SELECT
    'Vômito' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_vomiting = 'SIM'

UNION ALL

-- Fadiga
SELECT
    'Fadiga' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_fatigue = 'SIM'

UNION ALL

-- Perda de Olfato
SELECT
    'Perda de Olfato' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_loss_of_smell = 'SIM'

UNION ALL

-- Perda de Paladar
SELECT
    'Perda de Paladar' AS symptom_name,
    COUNT(CASE WHEN NOT required_icu = 'SIM' THEN 1 END) AS total_non_icu_cases,
    COUNT(CASE WHEN required_icu = 'SIM' THEN 1 END) AS total_icu_cases
FROM joined_data
WHERE had_loss_of_taste = 'SIM'

ORDER BY
    total_icu_cases DESC
