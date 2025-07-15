-- Cria uma dimensão para cada combinação única de fatores de risco (comorbidades).
WITH risk_factors AS (
    SELECT DISTINCT
        ("PUERPERA" = '1') AS is_puerpera,
        ("CARDIOPATI" = '1') AS has_chronic_cardiovascular_disease, 
        ("HEMATOLOGI" = '1') AS has_chronic_hematologic_disease, 
        ("SIND_DOWN" = '1') AS has_down_syndrome,
        ("HEPATICA" = '1') AS has_chronic_liver_disease,
        ("ASMA" = '1') AS has_asthma,
        ("DIABETES" = '1') AS has_diabetes,
        ("NEUROLOGIC" = '1') AS has_chronic_neurological_disease,
        ("PNEUMOPATI" = '1') AS has_other_chronic_pneumopathy,
        ("IMUNODEPRE" = '1') AS has_immunodeficiency,
        ("RENAL" = '1') AS has_chronic_kidney_disease,
        ("OBESIDADE" = '1') AS has_obesity
    FROM
        {{ source('opendatasus', 'opendatasus_srag_cases') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key([
        "is_puerpera", "has_chronic_cardiovascular_disease", "has_chronic_hematologic_disease", "has_down_syndrome", "has_chronic_liver_disease", "has_asthma",
        "has_diabetes", "has_chronic_neurological_disease", "has_other_chronic_pneumopathy", "has_immunodeficiency", "has_chronic_kidney_disease", "has_obesity"
    ]) }} AS risk_factors_id,
    
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
    has_obesity
FROM
    risk_factors