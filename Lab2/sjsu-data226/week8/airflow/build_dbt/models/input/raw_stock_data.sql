-- models/raw_stock_data.sql
SELECT
    date,
    symbol,
    CAST(open AS FLOAT) AS open,
    CAST(high AS FLOAT) AS high,
    CAST(low AS FLOAT) AS low,
    CAST(close AS FLOAT) AS close,
    CAST(volume AS INTEGER) AS volume
FROM {{ source('raw_data', 'STOCK_PRICE') }}
WHERE date >= CURRENT_DATE - INTERVAL '90 days'
