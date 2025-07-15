WITH source_data AS (
    SELECT
        'Código IBGE do Município',
        'Nome do Município',
        'Estado',
        'ID da Estação', 
        'Nome da Estação', 
        'Latitude', 
        'Longitude',
        'no_fonte_dados'
    FROM {{source("monitor_ar", "monitorar_stations")}}
),

-- Tratar e renomear os dados
renamed_and_casted AS (
    SELECT
        -- Limpa espaços e padroniza
        SUBSTRING(TRIM("Código IBGE do Município"), 1, 6) AS city_ibge_code,
        UPPER(TRIM("Nome do Município")) AS city_name,
        UPPER(TRIM("no_fonte_dados")) AS data_source_organization,
        UPPER(TRIM("Estado")) AS state_code,
        TRIM("ID da Estação") AS source_station_code,
        TRIM("Nome da Estação") AS station_name,
        -- Converte o separador de decimais para ponto, caso não seja null
        NULLIF(REPLACE("Latitude", ',', '.'), '')::NUMERIC AS latitude,
        NULLIF(REPLACE("Longitude", ',', '.'), '')::NUMERIC AS longitude,
    FROM
        source_data
)

SELECT
    -- Colunas que definem unicamente uma estação para gerar um ID.
    {{ dbt_utils.generate_surrogate_key(['source_station_code', 'data_source_organization']) }} AS station_id,
    
    city_ibge_code,
    city_name,
    state_code,
    source_station_code,
    station_name,
    data_source_organization,
    latitude,
    longitude

FROM
    renamed_and_casted
