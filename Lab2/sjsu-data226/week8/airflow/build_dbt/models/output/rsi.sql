WITH base AS (
    SELECT * 
    FROM {{ source('raw_data', 'STOCK_PRICE') }}
),
price_diff AS (
    SELECT
        date,
        symbol,
        close - LAG(close) OVER (PARTITION BY symbol ORDER BY date) AS price_change
    FROM base
),
gain_loss AS (
    SELECT
        date,
        symbol,
        CASE WHEN price_change > 0 THEN price_change ELSE 0 END AS gain,
        CASE WHEN price_change < 0 THEN ABS(price_change) ELSE 0 END AS loss
    FROM price_diff
),
average_gain_loss AS (
    SELECT
        date,
        symbol,
        AVG(gain) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 14 PRECEDING AND CURRENT ROW) AS avg_gain,
        AVG(loss) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 14 PRECEDING AND CURRENT ROW) AS avg_loss
    FROM gain_loss
),
rs AS (
    SELECT
        date,
        symbol,
        CASE 
            WHEN avg_loss = 0 THEN 100
            ELSE (avg_gain / avg_loss) 
        END AS rs
    FROM average_gain_loss
),
rsi AS (
    SELECT
        date,
        symbol,
        100 - (100 / (1 + rs)) AS rsi
    FROM rs
)
SELECT
    date,
    symbol,
    rsi
FROM rsi
ORDER BY symbol, date
