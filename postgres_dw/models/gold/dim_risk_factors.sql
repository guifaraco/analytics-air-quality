-- Cria uma dimensão para cada combinação única de fatores de risco (comorbidades).
WITH risk_factors AS (
    SELECT DISTINCT
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
        {{ ref('silver_srag_cases') }}
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