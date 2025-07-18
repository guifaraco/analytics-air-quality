-- Cria a dimensão de estações de monitoramento.

WITH silver_stations AS (
    SELECT
        station_business_key,
        station_id,
        source_station_code,
        station_name,
        city_ibge_code,
        city_name,
        state_code,
        latitude,
        longitude
    FROM
        {{ ref('silver_stations') }}
),

dim_locations AS (
    SELECT
        location_id,
        city_ibge_code
    FROM
        {{ ref('dim_locations') }}
)

-- Seleção Final
SELECT
    s.station_business_key,
    s.station_id AS monitoring_station_id,
    l.location_id,
    s.source_station_code,
    s.station_name,
    s.city_name,
    s.state_code,
    s.latitude,
    s.longitude
FROM
    silver_stations AS s
LEFT JOIN
    dim_locations AS l ON s.city_ibge_code = l.city_ibge_code