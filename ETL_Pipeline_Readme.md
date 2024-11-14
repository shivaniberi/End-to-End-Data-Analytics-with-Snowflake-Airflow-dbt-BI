
# ETL Pipeline and Data Analytics Project

## Problem Statement
This project demonstrates the creation of an ETL (Extract, Transform, Load) pipeline using Airflow, dbt, and a BI tool (e.g., Tableau, Superset, or Preset). It focuses on transforming raw stock market data, applying analytics like moving averages and RSI, and visualizing the results through a dashboard.

## Requirements and Specifications
- **Airflow**: To orchestrate the ETL pipeline, ensuring the data flows smoothly between systems.
- **dbt**: To handle the data transformation, implement models, snapshots, and tests.
- **BI Tool**: To create a dashboard for data visualization and provide business insights.
- **SQL Transactions with Idempotency**: To ensure data processing is repeatable and safe.

## Overall System Diagram
![System Diagram](path_to_image)

## Detailed Table Structures

### `moving_average.sql`
- **Fields**: `date`, `symbol`, `close`, `close_7d_avg`, `close_30d_avg`
- **Attributes**: `date` is the primary key, `symbol` is indexed.
- **Constraints**: `symbol` and `date` are mandatory, `close` and averages are numeric.

### `rsi.sql`
- **Fields**: `date`, `symbol`, `rsi`
- **Attributes**: `date`, `symbol` form the composite key.
- **Constraints**: `rsi` is a numeric value, `date` and `symbol` are unique together.

### `stock_analytics.sql`
- **Fields**: `date`, `symbol`, `close`, `close_7d_avg`, `close_30d_avg`, `rsi`
- **Attributes**: Combines fields from `moving_average` and `rsi`.
- **Constraints**: `symbol` and `date` are mandatory; unique combinations.

---

## Airflow Data Pipeline

### Code
- The Airflow DAG code is implemented in Python to schedule and manage tasks like data extraction, transformation, and loading.
- Tasks are structured using Airflow's `@task` decorator.

```python
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

@dag(schedule_interval="@daily", start_date=days_ago(1))
def data_pipeline():
    @task
    def extract_data():
        # Code to extract data
    
    @task
    def transform_data():
        # Code to transform data
    
    @task
    def load_data():
        # Code to load data into target system
    
    extract_data() >> transform_data() >> load_data()

# Execute the DAG
data_pipeline()
```

### Screenshot
![Airflow Web UI](path_to_airflow_ui_screenshot)

### Use of Airflow Connections and Variables
- Airflow connections and variables are used to manage API keys, database credentials, and configurations securely.
- SQL transactions are wrapped in try/catch blocks for idempotency, ensuring safe re-runs.

### SQL Transaction Example
```sql
BEGIN TRANSACTION;

TRY
    -- SQL operations here
COMMIT;

CATCH
    -- Handle errors
ROLLBACK;
```

---

## dbt Implementation

### Project Code
The dbt project is set up with models for transformation and snapshots for time-based analytics.
- Models: SQL files to transform raw data into usable tables.
- Tests: Ensuring data quality and consistency.
- Snapshot: Track changes to tables over time.

### Example Model
```sql
-- models/stock_analytics.sql
SELECT
    date,
    symbol,
    close,
    close_7d_avg,
    close_30d_avg,
    rsi.rsi
FROM {{ ref('moving_average') }} ma
JOIN {{ ref('rsi') }} rsi
ON ma.date = rsi.date AND ma.symbol = rsi.symbol;
```

### Commands
```bash
# Run dbt models
dbt run

# Test dbt models
dbt test

# Snapshot dbt models
dbt snapshot
```

### Screenshot of dbt Commands
![dbt Commands](path_to_dbt_command_screenshot)

---

## BI Tool (e.g., Tableau, Superset, or Preset)

### Dashboard Description
The dashboard visualizes stock market trends with metrics like moving averages and RSI over time. It allows users to analyze stock performance and detect trends.

- **Purpose**: To provide real-time insights into stock movements.
- **Usage**: Analysts can filter by symbol, date, and other parameters to explore historical stock performance.

### Dashboard Screenshots
1. **Chart 1 (e.g., Moving Averages)**  
   ![Chart 1](path_to_chart_1_screenshot)

2. **Chart 2 (e.g., RSI Trend)**  
   ![Chart 2](path_to_chart_2_screenshot)

3. **Filter Usage (e.g., Date Range)**  
   ![Date Range Filter](path_to_filter_screenshot)

---

## Conclusion
This project integrates multiple tools and technologies to create an end-to-end data pipeline. By using Airflow for orchestration, dbt for transformation, and a BI tool for visualization, the system processes stock market data into meaningful insights, ready for analysis and decision-making.
