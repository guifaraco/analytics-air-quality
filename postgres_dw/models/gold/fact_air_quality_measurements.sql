-- Cria a tabela de fatos para as medições de qualidade do ar.

WITH measurements AS (
    -- Seleciona os dados de medições já limpos da camada Silver
    SELECT
        station_business_key,
        measured_at,
        station_name,
        pollutant_code,
        pollutant_name,
        measurement_value
    FROM {{ ref('silver_measurements') }}
),

dim_stations AS (
    SELECT
        monitoring_station_id,
        station_business_key,
        station_name,
        location_id
    FROM {{ ref('dim_monitoring_stations') }}
),

dim_pollutants AS (
    SELECT
        pollutant_id,
        pollutant_code
    FROM {{ ref('dim_pollutants') }}
),

dim_date AS (
    SELECT
        date_id,
        full_date
    FROM {{ ref('dim_date') }}
)

SELECT
    -- Chaves
    d.date_id,
    s.monitoring_station_id,
    p.pollutant_id,
    s.location_id,
    -- Métrica
    m.measurement_value
FROM
    measurements AS m
-- JOIN para buscar a chave da dimensão de estações
LEFT JOIN dim_stations AS s
    ON m.station_business_key = s.station_business_key
-- JOIN para buscar a chave da dimensão de poluentes
LEFT JOIN dim_pollutants AS p
    ON m.pollutant_code = p.pollutant_code
-- JOIN para buscar a chave da dimensão de data
LEFT JOIN dim_date AS d
    ON CAST(m.measured_at AS DATE) = d.full_date
WHERE
    d.date_id IS NOT NULL
