WITH fact_air_quality_measurements AS (
    SELECT
        pollutant_id,
        date_id,
        location_id,
        measurement_value
    FROM
        {{ ref('fact_air_quality_measurements') }}
),

dim_date AS (
    SELECT
        date_id
    FROM
        {{ ref('dim_date') }}
),

dim_pollutants AS (
    SELECT
        pollutant_id,
        pollutant_code,
        measurement_unit
    FROM
        {{ ref('dim_pollutants') }}
),

dim_locations AS (
    SELECT
        location_id,
        state_code
    FROM
        {{ ref('dim_locations') }}
)

SELECT
    p.pollutant_code,
    p.measurement_unit,
    l.state_code,
    AVG(f.measurement_value) AS avg_pollution
FROM
    fact_air_quality_measurements f
JOIN
    dim_date d ON f.date_id = d.date_id
JOIN
    dim_pollutants p ON f.pollutant_id = p.pollutant_id
JOIN
    dim_locations l ON f.location_id = l.location_id
WHERE
    p.pollutant_code IN ('MP10', 'NO2', 'SO2', 'O3', 'CO', 'MP2,5')
GROUP BY
    p.pollutant_code,
    p.measurement_unit,
    l.state_code
ORDER BY
    p.pollutant_code,
    AVG(f.measurement_value) DESC
