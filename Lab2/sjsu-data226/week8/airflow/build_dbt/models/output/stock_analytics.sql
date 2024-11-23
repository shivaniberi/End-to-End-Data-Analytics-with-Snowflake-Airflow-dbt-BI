
-- models/stock_analytics.sql
{{ config(materialized='table') }}

-- models/stock_analytics.sql
SELECT
    ma.date,
    ma.symbol,
    ma.close,
    ma.close_7d_avg,
    ma.close_30d_avg,
    rsi.rsi
FROM {{ ref('moving_average') }} ma
JOIN {{ ref('rsi') }} rsi
ON ma.date = rsi.date AND ma.symbol = rsi.symbol
