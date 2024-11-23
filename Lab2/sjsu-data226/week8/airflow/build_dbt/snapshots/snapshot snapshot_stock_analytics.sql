{% snapshot snapshot_stock_analytics %}

{{
  config(
    target_schema='snapshot',
    unique_key='symbol',
    strategy='timestamp',
    updated_at='date',
    invalidate_hard_deletes=True
  )
}}

SELECT 
    date,
    symbol,
    close_7d_avg AS moving_average,  -- Use the correct column name
    rsi
FROM {{ ref('stock_analytics') }}

{% endsnapshot %}
