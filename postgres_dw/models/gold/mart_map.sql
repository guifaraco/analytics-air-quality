-- CTE para agregar os casos de saúde por localidade
WITH health_cases_by_location AS (
    SELECT
        f.location_id,
        SUM(f.case_count) AS total_health_cases
    FROM
        {{ ref('fact_health_cases') }} AS f
    JOIN
        {{ ref('dim_case_classifications') }} AS cc ON f.case_classification_id = cc.case_classification_id
    GROUP BY
        f.location_id
),

-- CTE para agregar as medições de poluição por localidade
air_quality_by_location AS (
    SELECT
        f.location_id,
        AVG(f.measurement_value) AS avg_pollution_value,
        COUNT(f.measurement_value) AS total_measurements
    FROM
        {{ ref('fact_air_quality_measurements') }} AS f
    GROUP BY
        f.location_id
),

-- CTE para obter as coordenadas de cada localidade.
locations_with_coords AS (
    SELECT
        l.location_id,
        l.city_name,
        l.state_code,
        -- Como uma cidade pode ter várias estações, calculamos a média das coordenadas.
        AVG(s.latitude) AS latitude,
        AVG(s.longitude) AS longitude
    FROM
        {{ ref('dim_locations') }} AS l
    LEFT JOIN
        {{ ref('dim_monitoring_stations') }} AS s ON l.location_id = s.location_id
    GROUP BY
        l.location_id,
        l.city_name,
        l.state_code
)

SELECT
    loc.location_id,
    loc.city_name,
    loc.state_code,
    loc.latitude,
    loc.longitude,

    -- Usamos COALESCE para garantir que, se uma cidade não tiver casos ou medições, o valor seja 0 em vez de NULL.
    COALESCE(hc.total_health_cases, 0) AS total_health_cases,
    COALESCE(aq.avg_pollution_value, 0) AS avg_pollution_value

FROM
    locations_with_coords AS loc

LEFT JOIN
    health_cases_by_location AS hc ON loc.location_id = hc.location_id

LEFT JOIN
    air_quality_by_location AS aq ON loc.location_id = aq.location_id
WHERE
    -- Garantimos que só apareçam no mapa as localidades que têm coordenadas
    loc.latitude IS NOT NULL
    AND loc.longitude IS NOT NULL
