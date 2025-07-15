-- Cria uma dimensão para cada combinação única de sintomas reportados.
WITH symptoms AS (
    SELECT DISTINCT
        ("FEBRE" = '1') AS had_fever,
        ("TOSSE" = '1') AS had_cough,
        ("GARGANTA" = '1') AS had_sore_throat,
        ("DISPNEIA" = '1') AS had_dyspnea,
        ("DESC_RESP" = '1') AS had_respiratory_distress,
        ("SATURACAO" = '1') AS had_low_saturation,
        ("DIARREIA" = '1') AS had_diarrhea,
        ("VOMITO" = '1') AS had_vomiting,
        ("FADIGA" = '1') AS had_fatigue,
        ("PERD_OLFT" = '1') AS had_loss_of_smell,
        ("PERD_PALA" = '1') AS had_loss_of_taste
    FROM
        {{ source('opendatasus', 'opendatasus_srag_cases') }}
)
SELECT
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