WITH source_data AS (
    SELECT 
        "Sigla", 
        "Item_monitorado",
        "Nome da Estação"
        "Data",
        "Hora"
        "Concentracao", 
        "iqar" 
    FROM {{source("monitor_ar", "monitorar_measurements")}}
),

pollutant_units_source AS (
    SELECT DISTINCT
        "sigla" AS pollutant_code,
        "pollutant_units" AS pollutant_units
    FROM
        {{ source('bronze', 'pollutant_units') }}

)

-- Tratar e renomear os dados
renamed_and_casted AS (
    SELECT
        -- Elimina os espaços em branco
        CASE 
            WHEN "Sigla" = "NH?" THEN REPLACE(UPPER(TRIM("Sigla")), "?", "3")
            WHEN "Sigla" = "CH?" THEN REPLACE(UPPER(TRIM("Sigla")), "?", "4")
            ELSE UPPER(TRIM("Sigla"))
        END AS pollutant_code,
        UPPER(TRIM("Item_monitorado")) AS pollutant_name,
        UPPER(TRIM("Nome da Estação")) AS station_name,
        -- Concatena as colunas 'data' e 'hora' para gerar um timestamp
        TO_TIMESTAMP("Data" || ' ' || "Hora", 'DD/MM/YYYY HH24:MI:SS') AS measured_at_utc,
        -- Converte o separador de decimais para ponto, caso não seja null esses valores
        NULLIF(REPLACE("Concentracao", ',', '.'), '')::NUMERIC AS measurement_value,
        NULLIF(REPLACE("iqar", ',', '.'), '')::NUMERIC AS air_quality_index

    FROM
        source_data
)

SELECT
    -- Gerando uma primary key composta de três colunas da tabela
    {{ dbt_utils.generate_surrogate_key(['station_name', 'pollutant_name', 'measured_at_utc']) }} AS measurement_id,
    
    measures.measured_at_utc,
    measures.station_name,
    measures.pollutant_code,
    measures.pollutant_name,
    measures.measurement_value,
    COALESCE(u.measurement_unit, 'N/A') AS measurement_unit,
    measures.air_quality_index
FROM
    renamed_and_casted as measures
LEFT JOIN
    pollutant_units_source as u
    ON measures.pollutant_code = u.pollutant_code
WHERE
    -- Validando dados que vão entrar na camada silver
    measurement_value IS NOT NULL
    AND measured_at_utc IS NOT NULL