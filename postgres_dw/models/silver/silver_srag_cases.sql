-- CTE para extrair os dados da camada bronze(raw data)
WITH source_data AS (
    SELECT DISTINCT
        "NU_NOTIFIC",
        "DT_NOTIFIC",
        "DT_SIN_PRI",
        "DT_NASC",
        "DT_EVOLUCA",
        "SG_UF",
        "CO_MUN_RES",
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
        "EVOLUCAO",
        "PUERPERA",
        "CARDIOPATI",
        "HEMATOLOGI",
        "SIND_DOWN",
        "HEPATICA",
        "ASMA",
        "DIABETES",
        "NEUROLOGIC",
        "PNEUMOPATI",
        "IMUNODEPRE",
        "RENAL",
        "OBESIDADE",
        "FEBRE",
        "TOSSE",
        "GARGANTA",
        "DISPNEIA",
        "DESC_RESP",
        "SATURACAO",
        "DIARREIA",
        "VOMITO",
        "FADIGA",
        "PERD_OLFT",
        "PERD_PALA"
    FROM
        {{ source('opendatasus', 'opendatasus_srag_cases') }}
),

-- CTE para transformar os dados
-- Padroniza o nome das colunas,
-- Faz o casting dos dados,
-- Limpa espaços vazios antes e depois da string,
-- Deixa os textos em maiusculo,
-- Tranforma algumas colunas categóricas, que estavam sendo representadas por números, para a string equivalente
cleaned_and_casted AS (
    SELECT
        TRIM("NU_NOTIFIC") AS notification_id,
        -- Tranforma em datas
        TO_DATE("DT_NOTIFIC", 'YYYY-MM-DD') AS notification_date,
        TO_DATE("DT_SIN_PRI", 'YYYY-MM-DD') AS first_symptoms_date,
        TO_DATE("DT_NASC", 'YYYY-MM-DD') AS birth_date,
        TO_DATE("DT_EVOLUCA", 'YYYY-MM-DD') AS outcome_date,
        TO_DATE("DT_INTERNA", 'YYYY-MM-DD') AS hospitalization_date,
        TO_DATE("DT_ENTUTI", 'YYYY-MM-DD') AS icu_entry_date,
        TO_DATE("DT_SAIDUTI", 'YYYY-MM-DD') AS icu_exit_date,

        -- Localização
        "CO_MUN_RES" AS residence_city_ibge_code,
        UPPER(TRIM("SG_UF")) AS residence_state_code,
        UPPER(TRIM("ID_MN_RESI")) AS residence_city_name,
        -- Decodificação Demográfica
        CASE "CS_SEXO"
            WHEN 'M' THEN 'MASCULINO'
            WHEN 'F' THEN 'FEMININO'
            ELSE 'IGNORADO'
        END AS gender,

        CASE "CS_RACA"
            WHEN '1' THEN 'BRANCA'
            WHEN '2' THEN 'PRETA'
            WHEN '3' THEN 'AMARELA'
            WHEN '4' THEN 'PARDA'
            WHEN '5' THEN 'INDIGENA'
            ELSE 'IGNORADO'
        END AS race,

        -- Decodificação da Escolaridade
        CASE "CS_ESCOL_N"
            WHEN '0' THEN 'SEM ESCOLARIDADE'
            WHEN '1' THEN 'FUNDAMENTAL1'
            WHEN '2' THEN 'FUNDAMENTAL2'
            WHEN '3' THEN 'ENSINO MEDIO'
            WHEN '4' THEN 'ENSINO SUPERIOR'
            WHEN '5' THEN 'NAO SE APLICA'
            ELSE 'IGNORADO'
        END AS education_level,

         -- TRATAMENTO DOS SINTOMAS
        CASE "FEBRE"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_fever,

        CASE "TOSSE"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_cough,

        CASE "GARGANTA"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_sore_throat,

        CASE "DISPNEIA"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_dyspnea,

        CASE "DESC_RESP"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_respiratory_distress,

        CASE "SATURACAO"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_low_saturation,

        CASE "DIARREIA"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_diarrhea,

        CASE "VOMITO"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_vomiting,

        CASE "FADIGA"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_fatigue,

        CASE "PERD_OLFT"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_loss_of_smell,

        CASE "PERD_PALA"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS had_loss_of_taste,

        -- TRATAMENTO DOS FATORES DE RISCO
        CASE "PUERPERA"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS is_puerpera,

        CASE "CARDIOPATI"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_chronic_cardiovascular_disease,

        CASE "HEMATOLOGI"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_chronic_hematologic_disease,

        CASE "SIND_DOWN"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_down_syndrome,

        CASE "HEPATICA"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_chronic_liver_disease,

        CASE "ASMA"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_asthma,

        CASE "DIABETES"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_diabetes,

        CASE "NEUROLOGIC"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_chronic_neurological_disease,

        CASE "PNEUMOPATI"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_other_chronic_pneumopathy,

        CASE "IMUNODEPRE"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_immunodeficiency,

        CASE "RENAL"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_chronic_kidney_disease,

        CASE "OBESIDADE"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_obesity,


        -- Decodificação Clínica
        CASE "FATOR_RISC"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS has_risk_factors,

        CASE "HOSPITAL"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS was_hospitalized,

        CASE "UTI"
            WHEN '1' THEN 'SIM'
            WHEN '2' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS required_icu,

        CASE "SUPORT_VEN"
            WHEN '1' THEN 'INVASIVO'
            WHEN '2' THEN 'NAO INVASIVO'
            WHEN '3' THEN 'NAO'
            ELSE 'IGNORADO'
        END AS ventilatory_support_type,

        -- Decodificação da Classificação Final
        CASE "CLASSI_FIN"
            WHEN '1' THEN 'SRAG POR INFLUENZA'
            WHEN '2' THEN 'SRAG POR OUTRO VIRUS RESPIRATORIO'
            WHEN '3' THEN 'SRAG POR OUTRO AGENTE ETIOLOGICO'
            WHEN '4' THEN 'SRAG NAO ESPECIFICADO'
            WHEN '5' THEN 'SRAG POR COVID-19'
            ELSE 'IGNORADO'
        END AS final_classification,

        -- Decodificação do Critério de Encerramento
        CASE "CRITERIO"
            WHEN '1' THEN 'LABORATORIAL'
            WHEN '2' THEN 'CLINICO EPIDEMOLOGICO'
            WHEN '3' THEN 'CLINICO'
            WHEN '4' THEN 'CLINICO IMAGEM'
            ELSE 'IGNORADO'
        END AS closure_criteria,

        -- Decodificação da Evolução do caso
        CASE "EVOLUCAO"
            WHEN '1' THEN 'CURA'
            WHEN '2' THEN 'OBITO'
            WHEN '3' THEN 'OBITO POR OUTRAS CAUSAS'
            ELSE 'IGNORADO'
        END AS case_outcome
    FROM
        source_data
)

SELECT
    -- Gera a chave primária
    {{ dbt_utils.generate_surrogate_key(['notification_id']) }} AS health_case_id,

    -- Gera uma chave única para cada combinação de valores diferentes
    {{ dbt_utils.generate_surrogate_key([
        'had_fever', 'had_cough', 'had_sore_throat', 'had_dyspnea', 'had_respiratory_distress',
        'had_low_saturation', 'had_diarrhea', 'had_vomiting', 'had_fatigue',
        'had_loss_of_smell', 'had_loss_of_taste'
    ]) }} AS symptoms_id,
    -- Mesma coisa que o symptoms_id
    {{ dbt_utils.generate_surrogate_key([
            'is_puerpera', 'has_chronic_cardiovascular_disease', 'has_chronic_hematologic_disease',
            'has_down_syndrome', 'has_chronic_liver_disease', 'has_asthma', 'has_diabetes',
            'has_chronic_neurological_disease', 'has_other_chronic_pneumopathy',
            'has_immunodeficiency', 'has_chronic_kidney_disease', 'has_obesity'
    ]) }} AS risk_factors_id,

    notification_id,
    notification_date,
    first_symptoms_date,
    birth_date,
    outcome_date,
    residence_city_ibge_code,
    residence_city_name,
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
    had_fever,
    had_cough,
    had_sore_throat,
    had_dyspnea,
    had_respiratory_distress,
    had_low_saturation,
    had_diarrhea,
    had_vomiting,
    had_fatigue,
    had_loss_of_smell,
    had_loss_of_taste,
    is_puerpera,
    has_chronic_cardiovascular_disease,
    has_chronic_hematologic_disease,
    has_down_syndrome,
    has_chronic_liver_disease,
    has_asthma,
    has_diabetes,
    has_chronic_neurological_disease,
    has_other_chronic_pneumopathy,
    has_immunodeficiency,
    has_chronic_kidney_disease,
    has_obesity,
    1 AS case_count -- Contagem de casos

FROM
    cleaned_and_casted
WHERE
    notification_id IS NOT NULL
        AND
    birth_date IS NOT NULL
        AND
    notification_date IS NOT NULL
        AND
    residence_city_ibge_code IS NOT NULL
        AND
    residence_city_name IS NOT NULL
