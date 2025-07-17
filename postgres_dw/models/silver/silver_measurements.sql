WITH source_data AS (
    -- Seleciona os dados da fonte principal de medições
    SELECT 
        "Estado",
        "Nome do Município",
        "Nome da Estação",
        "Data",
        "Hora",
        "Sigla",
        "Item_monitorado" AS pollutant_name_source,
        "Concentracao", 
        "iqar" AS air_quality_index
    FROM 
        {{ source("monitor_ar", "monitorar_measurements") }}
),

pollutant_units_source AS (
    -- Seleciona os dados da fonte de unidades
    SELECT DISTINCT
        "sigla" AS pollutant_code,
        "pollutant_units" AS measurement_unit
    FROM
        {{ source('monitor_ar', 'pollutant_units') }}
),

-- Juntamos as duas fontes
enriched_data AS (
    SELECT
        s.*, -- Pega todas as colunas da fonte principal
        u.measurement_unit -- Adiciona a coluna de unidade do JOIN
    FROM
        source_data AS s
    LEFT JOIN 
        pollutant_units_source AS u ON TRIM(UPPER(s."Sigla")) = u.pollutant_code
),

renamed_and_casted AS (
    -- Limpa os dados
    SELECT
        TRIM(UPPER("Estado")) AS state_code,
        TRIM(UPPER("Nome do Município")) AS city_name,
        TRIM(UPPER("Nome da Estação")) AS station_name,
        TRIM(UPPER("Sigla")) AS pollutant_code,
        TRIM(UPPER("pollutant_name_source")) AS pollutant_name,
        TO_TIMESTAMP("Data" || ' ' || "Hora", 'DD/MM/YYYY HH24:MI:SS') AS measured_at,
        "Concentracao"::NUMERIC AS measurement_value,
        -- Usamos COALESCE para tratar casos onde o JOIN não encontrou uma unidade
        COALESCE(measurement_unit, 'N/A') AS measurement_unit
    FROM
        enriched_data
),

-- 5. DE-DUPLICAÇÃO: Aplicamos o ROW_NUMBER na tabela
deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER(
            PARTITION BY state_code, city_name, station_name, measured_at, pollutant_name
            ORDER BY measured_at
        ) as duplicate_rank
    FROM
        renamed_and_casted
)

SELECT
    state_code || '-' || city_name || '-' || station_name AS station_business_key,
    {{ dbt_utils.generate_surrogate_key(['state_code', 'city_name', 'station_name', 'measured_at', 'pollutant_name']) }} AS measurement_id,
    state_code,
    measured_at,
    station_name,
    pollutant_code,
    pollutant_name,
    measurement_value,
    measurement_unit
FROM
    deduplicated
WHERE
    duplicate_rank = 1
    AND measurement_value IS NOT NULL
    AND measurement_value >= 0.1
    AND measurement_value < 200
    AND measured_at IS NOT NULL