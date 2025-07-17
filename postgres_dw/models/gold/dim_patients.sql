-- Cria a dimensão de pacientes, agrupando perfis demográficos únicos.

WITH patient_profiles AS (
    SELECT DISTINCT
        gender,
        race,
        education_level,
        -- Calculamos a idade atual ou no momento da notificação para criar faixas etárias
        DATE_PART('year', AGE(notification_date, birth_date)) AS age_at_notification
    FROM
        {{ ref('silver_srag_cases') }}
)
SELECT
    -- Chave primária para o perfil do paciente
    {{ dbt_utils.generate_surrogate_key(['gender', 'race', 'education_level', 'age_at_notification']) }} AS patient_id,

    gender,
    race,
    education_level,
    age_at_notification,

    -- Criação de faixas etárias
    CASE
        WHEN age_at_notification <= 4 THEN '0-4 ANOS'
        WHEN age_at_notification <= 9 THEN '5-9 ANOS'
        WHEN age_at_notification <= 19 THEN '10-19 ANOS'
        WHEN age_at_notification <= 29 THEN '20-29 ANOS'
        WHEN age_at_notification <= 39 THEN '30-39 ANOS'
        WHEN age_at_notification <= 49 THEN '40-49 ANOS'
        WHEN age_at_notification <= 59 THEN '50-59 ANOS'
        ELSE '60+ ANOS'
    END AS age_group

FROM
    patient_profiles