-- Cria a dimensão de localidades.

-- Pega as localidades únicas das estações de monitoramento
WITH monitorar_locations AS (
    SELECT
        city_ibge_code,
        city_name,
        state_code
    FROM
        {{ ref('silver_stations') }}
),

-- Pega as localidades únicas dos casos de SRAG
srag_locations AS (
    SELECT
        residence_city_ibge_code AS city_ibge_code,
        residence_city_name AS city_name,
        residence_state_code AS state_code
    FROM
        {{ ref('silver_srag_cases') }}
),
-- JOIN das duas CTEs para pegar todas as localizações que são em comum
all_locations_unioned AS (
    SELECT DISTINCT
        m.city_ibge_code,
        m.city_name,
        m.state_code
    FROM monitorar_locations as m
    JOIN srag_locations as s ON m.city_ibge_code = s.city_ibge_code
)

SELECT
    -- Gera a chave primária a partir do código IBGE, que é um identificador único para municípios.
    {{ dbt_utils.generate_surrogate_key(['city_ibge_code']) }} AS location_id,
    city_ibge_code,
    city_name,
    state_code
FROM
    all_locations_unioned
WHERE
    city_ibge_code IS NOT NULL
