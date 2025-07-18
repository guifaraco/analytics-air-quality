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

 dim_symptoms AS (
    SELECT * FROM {{ ref('dim_symptoms') }}
),

 dim_risk_factors AS (
    SELECT * FROM {{ ref('dim_risk_factors') }}
),

 dim_case_classifications AS (
    SELECT * FROM {{ ref('dim_case_classifications') }}
),

dim_date_notification AS (
    SELECT date_id, full_date FROM {{ ref('dim_date') }}
),

dim_date_symptoms AS (
    SELECT date_id, full_date FROM {{ ref('dim_date') }}
)

SELECT
    -- Chave primária
    s.health_case_id,

    -- Chaves Estrangeiras - As "ligações"
    d_notification.date_id AS notification_date_id,
    d_symptoms.date_id AS first_symptoms_date_id,
    loc.location_id,
    p.patient_id,
    sym.symptoms_id,
    rf.risk_factors_id,
    cc.case_classification_id,

    -- Métricas e flags importantes
    s.was_hospitalized,
    s.required_icu,
    s.case_count

FROM
    silver_cases AS s

-- JOIN para buscar a chave de localidade
LEFT JOIN dim_locations AS loc
    ON s.residence_city_ibge_code = loc.city_ibge_code

-- JOIN para buscar a chave do perfil demográfico do paciente
LEFT JOIN dim_patients AS p
    ON s.gender = p.gender
    AND s.race = p.race
    AND s.education_level = p.education_level
    AND DATE_PART('year', AGE(s.notification_date, s.birth_date)) = p.age_at_notification

-- JOIN para buscar a chave do perfil de sintomas
LEFT JOIN dim_symptoms AS sym ON
    s.had_fever = sym.had_fever
    AND s.had_cough = sym.had_cough
    AND s.had_sore_throat = sym.had_sore_throat
    AND s.had_dyspnea = sym.had_dyspnea
    AND s.had_respiratory_distress = sym.had_respiratory_distress
    AND s.had_low_saturation = sym.had_low_saturation
    AND s.had_diarrhea = sym.had_diarrhea
    AND s.had_vomiting = sym.had_vomiting
    AND s.had_fatigue = sym.had_fatigue
    AND s.had_loss_of_smell = sym.had_loss_of_smell
    AND s.had_loss_of_taste = sym.had_loss_of_taste

-- JOIN para buscar a chave do perfil de fatores de risco
LEFT JOIN dim_risk_factors AS rf ON
    s.is_puerpera = rf.is_puerpera
    AND s.has_chronic_cardiovascular_disease = rf.has_chronic_cardiovascular_disease
    AND s.has_chronic_hematologic_disease = rf.has_chronic_hematologic_disease
    AND s.has_down_syndrome = rf.has_down_syndrome
    AND s.has_chronic_liver_disease = rf.has_chronic_liver_disease
    AND s.has_asthma = rf.has_asthma
    AND s.has_diabetes = rf.has_diabetes
    AND s.has_chronic_neurological_disease = rf.has_chronic_neurological_disease
    AND s.has_other_chronic_pneumopathy = rf.has_other_chronic_pneumopathy
    AND s.has_immunodeficiency = rf.has_immunodeficiency
    AND s.has_chronic_kidney_disease = rf.has_chronic_kidney_disease
    AND s.has_obesity = rf.has_obesity
-- JOIN para buscar a chave da classificação do caso
LEFT JOIN dim_case_classifications AS cc
    ON s.final_classification = cc.final_classification AND s.case_outcome = cc.case_outcome
-- JOINs para as datas
LEFT JOIN dim_date_notification AS d_notification ON s.notification_date = d_notification.full_date
LEFT JOIN dim_date_symptoms AS d_symptoms ON s.first_symptoms_date = d_symptoms.full_date
