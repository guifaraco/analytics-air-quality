-- Cria a tabela de fatos para os casos de SRAG, conectando um evento a todas as suas dimensões.

WITH silver_cases AS (
    SELECT * FROM {{ ref('silver_srag_cases') }}
),

-- Selecionamos as chaves de cada dimensão para os JOINs
 dim_locations AS (
    SELECT location_id, city_ibge_code FROM {{ ref('dim_locations') }}
),

dim_patients AS (
    SELECT * FROM {{ ref('dim_patients') }}
),

dim_case_classifications AS (
    SELECT * FROM {{ ref('dim_case_classifications') }}
),

dim_date AS (
    SELECT date_id, full_date FROM {{ ref('dim_date') }}
)

SELECT
    -- Chave primária
    s.health_case_id,

    -- Chaves Estrangeiras
    d_symptoms.date_id AS first_symptoms_date_id,
    loc.location_id,
    p.patient_id,
    s.symptoms_id,
    s.risk_factors_id,
    cc.case_classification_id,

    -- Métricas e flags importantes
    s.was_hospitalized,
    s.required_icu,
    s.case_count

FROM
    silver_cases AS s
-- JOIN para buscar a chave de localidade
JOIN dim_locations AS loc
    ON s.residence_city_ibge_code = loc.city_ibge_code
-- JOIN para buscar a chave do perfil demográfico do paciente
LEFT JOIN dim_patients AS p
    ON s.gender = p.gender
    AND s.race = p.race
    AND s.education_level = p.education_level
    AND DATE_PART('year', AGE(s.notification_date, s.birth_date)) = p.age_at_notification
-- JOIN para buscar a chave da classificação do caso
LEFT JOIN dim_case_classifications AS cc
    ON s.final_classification = cc.final_classification AND s.case_outcome = cc.case_outcome and s.closure_criteria = cc.closure_criteria
-- JOINs para as datas
LEFT JOIN dim_date AS d_symptoms ON s.first_symptoms_date = d_symptoms.full_date
