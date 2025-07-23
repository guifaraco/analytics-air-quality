WITH health_cases AS (
    SELECT 
        case_count,
        first_symptoms_date_id,
        location_id
    FROM
        {{ ref('fact_health_cases') }}
),

dim_date AS (
    SELECT 
        date_id,
        month
    FROM
        {{ ref('dim_date') }}
),

dim_locations AS (
    SELECT
        location_id,
        state_code
    FROM
        {{ ref('dim_locations') }}
)

SELECT
	SUM(hc.case_count),
	dt.month,
    l.state_code
FROM health_cases AS hc
JOIN dim_date AS dt
	ON hc.first_symptoms_date_id  = dt.date_id
JOIN dim_locations AS l
    ON hc.location_id = l.location_id
GROUP BY 
    dt.month,
    l.state_code
ORDER BY dt.month
