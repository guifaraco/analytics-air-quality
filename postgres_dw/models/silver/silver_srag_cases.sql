WITH source_data AS (
    SELECT
        "NU_NOTIFIC",
        "DT_NOTIFIC",
        "DT_SIN_PRI",
        "DT_NASC",
        "DT_EVOLUCA",
        "SG_UF",
        "ID_MN_RESI",
        "CS_SEXO",
        "CS_RACA",
        "CS_ESCOL_N",
        "FATOR_RISC",
        "HOSPITAL",
        "DT_INTERNA",
        "UTI",
        "DT_ENTUTI",
        "DT_SAIDUTI",
        "SUPORT_VEN",
        "CLASSI_FIN",
        "CRITERIO",
        "EVOLUCAO"
    FROM
        {{ source('opendatasus', 'opendatasus_srag_cases') }}
),

cleaned_and_casted AS (
    SELECT
        TRIM("NU_NOTIFIC") AS notification_id,
        -- Datas
        TO_DATE("DT_NOTIFIC", 'YYYY-MM-DD') AS notification_date,
        TO_DATE("DT_SIN_PRI", 'YYYY-MM-DD') AS first_symptoms_date,
        TO_DATE("DT_NASC", 'YYYY-MM-DD') AS birth_date,
        TO_DATE("DT_EVOLUCA", 'YYYY-MM-DD') AS outcome_date,
        TO_DATE("DT_INTERNA", 'YYYY-MM-DD') AS hospitalization_date,
        TO_DATE("DT_ENTUTI", 'YYYY-MM-DD') AS icu_entry_date,
        TO_DATE("DT_SAIDUTI", 'YYYY-MM-DD') AS icu_exit_date,

        -- Localização
        "ID_MN_RESI" AS residence_city_ibge_code,
        "SG_UF" AS residence_state_code,

        -- Decodificação Demográfica
        CASE "CS_SEXO" 
            WHEN '1' THEN 'Masculino' 
            WHEN '2' THEN 'Feminino' 
            ELSE 'Ignorado' 
        END AS gender,

        CASE "CS_RACA" 
            WHEN '1' THEN 'Branca' 
            WHEN '2' THEN 'Preta' 
            WHEN '3' THEN 'Amarela' 
            WHEN '4' THEN 'Parda' 
            WHEN '5' THEN 'Indígena' 
            ELSE 'Ignorado' 
        END AS race,
        
        -- Decodificação da Escolaridade
        CASE "CS_ESCOL_N"
            WHEN '0' THEN 'Sem escolaridade/Analfabeto'
            WHEN '1' THEN 'Fundamental 1º ciclo (1ª a 5ª série)'
            WHEN '2' THEN 'Fundamental 2º ciclo (6ª a 9ª série)'
            WHEN '3' THEN 'Médio (1º ao 3º ano)'
            WHEN '4' THEN 'Superior'
            WHEN '5' THEN 'Não se aplica'
            ELSE 'Ignorado'
        END AS education_level,

        -- Decodificação Clínica
        ("FATOR_RISC" = '1') AS has_risk_factors,
        ("HOSPITAL" = '1') AS was_hospitalized,
        ("UTI" = '1') AS required_icu,
        CASE "SUPORT_VEN" 
            WHEN '1' THEN 'Invasivo' 
            WHEN '2' THEN 'Não Invasivo' 
            WHEN '3' THEN 'Não' 
            ELSE 'Ignorado' 
        END AS ventilatory_support_type,
        
        -- Decodificação da Classificação Final
        CASE "CLASSI_FIN"
            WHEN '1' THEN 'SRAG por Influenza'
            WHEN '2' THEN 'SRAG por outro vírus respiratório'
            WHEN '3' THEN 'SRAG por outro agente etiológico'
            WHEN '4' THEN 'SRAG não especificado'
            WHEN '5' THEN 'SRAG por COVID-19'
            ELSE 'Não preenchido'
        END AS final_classification,

        -- Decodificação do Critério de Encerramento
        CASE "CRITERIO"
            WHEN '1' THEN 'Laboratorial'
            WHEN '2' THEN 'Clínico Epidemiológico'
            WHEN '3' THEN 'Clínico'
            WHEN '4' THEN 'Clínico Imagem'
            ELSE 'Não preenchido'
        END AS closure_criteria,

        -- Decodificação da Evolução do caso
        CASE "EVOLUCAO" 
            WHEN '1' THEN 'Cura' 
            WHEN '2' THEN 'Óbito' 
            WHEN '3' THEN 'Óbito por outras causas' 
            ELSE 'Ignorado' 
        END AS case_outcome
    FROM
        source_data
)

SELECT
    -- Gera a chave primária
    {{ dbt_utils.generate_surrogate_key(['notification_id']) }} AS health_case_id,
    
    notification_id,
    notification_date,
    first_symptoms_date,
    birth_date,
    outcome_date,
    residence_city_ibge_code,
    residence_state_code,
    gender,
    race,
    education_level,
    was_hospitalized,
    required_icu,
    ventilatory_support_type,
    final_classification,
    closure_criteria,
    case_outcome,
    1 AS case_count -- Contagem de casos

FROM
    cleaned_and_casted
WHERE
    notification_id IS NOT NULL

