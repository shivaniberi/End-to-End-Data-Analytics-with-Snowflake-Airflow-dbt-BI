
-- models/moving_average.sql
{{ config(materialized='table') }}

WITH base AS (
    SELECT * FROM {{ source('raw_data', 'STOCK_PRICE') }}
)
SELECT
    date,
    symbol,
    close,
    AVG(close) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS close_7d_avg,
    AVG(close) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS close_30d_avg
FROM base
