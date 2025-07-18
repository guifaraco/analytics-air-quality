-- Este modelo limpa os dados das estações.

WITH source_data AS (
    SELECT
        "ID da Estação" AS source_station_code,
        TRIM(UPPER("Nome da Estação")) AS station_name,
        TRIM(UPPER("Nome do Município")) AS city_name,
        TRIM(UPPER("Estado")) AS state_code,
        SUBSTRING(TRIM("Código IBGE do Município"), 1, 6) AS city_ibge_code,
        UPPER(TRIM("no_fonte_dados")) AS data_source_organization,
        NULLIF(REPLACE("Latitude", ',', '.'), '')::NUMERIC AS latitude,
        NULLIF(REPLACE("Longitude", ',', '.'), '')::NUMERIC AS longitude
        -- Adicione outras colunas da fonte de estações aqui
    FROM
        {{ source('monitor_ar', 'monitorar_stations') }}
),

-- Etapa para numerar e identificar as duplicatas
deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER(
            PARTITION BY state_code, city_name, station_name
            ORDER BY source_station_code
        ) as duplicate_rank
    FROM
        source_data
)

SELECT
    -- Criamos a chave de negócio
    state_code || '-' || city_name || '-' || station_name AS station_business_key,
    
    -- Criamos a chave primária
    {{ dbt_utils.generate_surrogate_key(['state_code', 'city_name', 'station_name']) }} AS station_id,
    
    source_station_code,
    data_source_organization,
    station_name,
    city_ibge_code,
    city_name,
    state_code,
    latitude,
    longitude
FROM
    deduplicated
WHERE
    duplicate_rank = 1
