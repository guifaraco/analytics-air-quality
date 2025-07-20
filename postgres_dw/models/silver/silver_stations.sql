-- Este modelo limpa os dados das estações.

WITH source_data AS (
    SELECT DISTINCT
        "Código IBGE do Município",
        "Nome do Município",
        "Estado",
        "ID da Estação",
        "Nome da Estação",
        "Latitude",
        "Longitude",
        "no_fonte_dados"
    FROM {{source("monitor_ar", "monitorar_stations")}}
),

renamed_and_casted AS (
    SELECT
        TRIM(UPPER("Nome da Estação")) AS station_name,
        TRIM(UPPER("Nome do Município")) AS city_name,
        TRIM(UPPER("Estado")) AS state_code,
        SUBSTRING(TRIM("Código IBGE do Município"), 1, 6) AS city_ibge_code,
        UPPER(TRIM("no_fonte_dados")) AS data_source_organization,
        NULLIF(REPLACE("Latitude", ',', '.'), '')::NUMERIC AS latitude,
        NULLIF(REPLACE("Longitude", ',', '.'), '')::NUMERIC AS longitude
    FROM
        source_data
)

SELECT
    -- Criamos a chave primária
    {{ dbt_utils.generate_surrogate_key(['city_ibge_code', 'station_name']) }} AS station_id,

    -- Criamos a chave de negócio
    state_code || '-' || city_name || '-' || station_name AS station_business_key,

    data_source_organization,
    station_name,
    city_ibge_code,
    city_name,
    state_code,
    latitude,
    longitude
FROM
    renamed_and_casted
