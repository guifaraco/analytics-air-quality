-- Este Data Mart une os dados das diferentes sources por ESTADO e MÊS.

-- CTE para os casos de saúde.
WITH health_cases_monthly AS (
    SELECT
        -- Criamos a chave de agregação para o mês (ex: '2022-07')
        TO_CHAR(d.full_date, 'YYYY-MM') AS year_month,
        -- Buscamos o state_code da dimensão de localidades
        l.state_code,
        -- Soma todos os casos daquele mês e estado
        SUM(hc.case_count) AS total_health_cases
    FROM
        {{ ref('fact_health_cases') }} AS hc
    LEFT JOIN
        {{ ref('dim_date') }} AS d ON hc.notification_date_id = d.date_id
    LEFT JOIN
        {{ ref('dim_locations') }} AS l ON hc.location_id = l.location_id
    WHERE
        l.state_code IS NOT NULL
    GROUP BY
        year_month, l.state_code -- Agrupa por ano/mês e estado
),

-- CTE para a qualidade do ar, também agregada por MÊS e ESTADO
air_quality_monthly_avg AS (
    SELECT
        -- Criamos a mesma chave para o mês
        TO_CHAR(d.full_date, 'YYYY-MM') AS year_month,
        -- Buscamos o state_code da dimensão de localidades
        l.state_code,
        p.pollutant_code,
        -- Calculamos a média mensal do poluente para o estado
        AVG(f.measurement_value) AS monthly_avg_pollution
    FROM
        {{ ref('fact_air_quality_measurements') }} AS f
    LEFT JOIN
        {{ ref('dim_pollutants') }} AS p ON f.pollutant_id = p.pollutant_id
    LEFT JOIN
        {{ ref('dim_date') }} AS d ON f.date_id = d.date_id
    LEFT JOIN
        {{ ref('dim_locations') }} AS l ON f.location_id = l.location_id
    WHERE
        p.pollutant_code IN ('MP2.5', 'SO2', 'NO2', 'MP10', 'CO', 'O3')
        AND l.state_code IS NOT NULL
    GROUP BY
        year_month, l.state_code, p.pollutant_code -- Agrupa por ano/mês, estado e poluente
)

SELECT
    h.year_month,
    h.state_code,
    a.pollutant_code,
    h.total_health_cases,
    a.monthly_avg_pollution

FROM
    health_cases_monthly AS h

-- O INNER JOIN garante que só teremos resultados para mês/estado que
-- existem em AMBAS as tabelas de métricas.
INNER JOIN air_quality_monthly_avg AS a
    ON h.year_month = a.year_month
    AND h.state_code = a.state_code

ORDER BY
    h.state_code,
    h.year_month,
    a.pollutant_code
