-- Cria a dimensão de estações de monitoramento.

-- Pega as colunas relevantes da ref silver_stations
WITH silver_stations AS (
    SELECT
        station_business_key,
        station_id,
        station_name,
        city_ibge_code,
        city_name,
        state_code,
        latitude,
        longitude
    FROM
        {{ ref('silver_stations') }}
),

-- Pega as colunas relevantes da ref dim_locations
dim_locations AS (
    SELECT
        location_id,
        city_ibge_code
    FROM
        {{ ref('dim_locations') }}
)

SELECT
    s.station_id AS monitoring_station_id,
    s.station_business_key,
    l.location_id,
    s.station_name,
    s.city_name,
    s.state_code,
    s.latitude,
    s.longitude
FROM
    silver_stations AS s
JOIN
    dim_locations AS l ON s.city_ibge_code = l.city_ibge_code
