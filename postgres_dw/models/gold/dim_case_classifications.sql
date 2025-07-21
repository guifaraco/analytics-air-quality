-- Cria a dimensão que descreve o diagnóstico e o desfecho final do caso.
WITH classifications AS (
    SELECT DISTINCT
        final_classification,
        closure_criteria,
        case_outcome
    FROM
        {{ ref('silver_srag_cases') }}
)
SELECT
    -- Cria uma chave primária com as colunas ['final_classification', 'closure_criteria', 'case_outcome']
    {{ dbt_utils.generate_surrogate_key(['final_classification', 'closure_criteria', 'case_outcome']) }} AS case_classification_id,
    final_classification,
    closure_criteria,
    case_outcome
FROM
    classifications
