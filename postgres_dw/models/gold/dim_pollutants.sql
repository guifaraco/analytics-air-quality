-- Cria a dimensão de poluentes, com uma linha para cada tipo de poluente único.

-- Selecionar todos os poluentes
WITH silver_measurements AS (
    SELECT DISTINCT
        pollutant_name,
        pollutant_code,
        measurement_unit
    FROM
        {{ ref('silver_measurements') }}
)

SELECT
    -- Cria a chave primária da dimensão a partir do código do poluente
    {{ dbt_utils.generate_surrogate_key(['pollutant_code']) }} AS pollutant_id,

    pollutant_code,
    pollutant_name,
    measurement_unit
FROM
    silver_measurements
WHERE
    pollutant_name IS NOT NULL
