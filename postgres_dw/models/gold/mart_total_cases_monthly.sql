WITH health_cases AS (
    SELECT case_count, first_symptoms_date_id
    FROM
        {{ ref('fact_health_cases') }}
),

dim_date AS (
    SELECT date_id, month
    FROM
        {{ ref('dim_date') }}
)

SELECT
	SUM(hc.case_count),
	dt.month
FROM health_cases AS hc
JOIN dim_date AS dt
	ON hc.first_symptoms_date_id  = dt.date_id
GROUP BY dt.month
ORDER BY dt.month
