-- Cria uma dimensão para cada combinação única de sintomas reportados.
WITH symptoms AS (
    -- Seleciona somente as combinações de valores distintas em relação as colunas selecionadas
    SELECT DISTINCT
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
        had_loss_of_taste
    FROM
        {{ ref('silver_srag_cases') }}
)
SELECT
    -- chave primária
    {{ dbt_utils.generate_surrogate_key([
        "had_fever", "had_cough", "had_sore_throat", "had_dyspnea", "had_respiratory_distress",
        "had_low_saturation", "had_diarrhea", "had_vomiting", "had_fatigue", "had_loss_of_smell", "had_loss_of_taste"
    ]) }} AS symptoms_id,

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
    had_loss_of_taste
FROM
    symptoms