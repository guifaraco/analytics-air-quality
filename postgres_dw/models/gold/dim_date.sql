-- Este modelo cria uma dimensão de data completa, com várias colunas úteis para análise.

-- Usamos a função generate_series para criar uma linha para cada dia em um intervalo.
WITH date_series AS (
    SELECT
        CAST(series.date AS DATE) AS full_date
    FROM
        GENERATE_SERIES('2022-01-01'::date, '2022-12-31'::date, '1 day'::interval) AS series(date)
)

-- A partir da lista de datas, extraímos todos os atributos que queremos.
SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::INTEGER AS date_id, -- Chave Primária
    full_date,
    EXTRACT(YEAR FROM full_date) AS year,
    EXTRACT(MONTH FROM full_date) AS month,
    EXTRACT(DAY FROM full_date) AS day,
    EXTRACT(QUARTER FROM full_date) AS quarter,
    TO_CHAR(full_date, 'TMDay') AS day_of_week, -- TMDay retorna o nome do dia da semana
    TO_CHAR(full_date, 'TMMonth') AS month_name, -- TMMonth retorna o nome do mês
    EXTRACT(ISODOW FROM full_date) IN (6, 7) AS is_weekend -- ISODOW: 6=Sábado, 7=Domingo
FROM
    date_series