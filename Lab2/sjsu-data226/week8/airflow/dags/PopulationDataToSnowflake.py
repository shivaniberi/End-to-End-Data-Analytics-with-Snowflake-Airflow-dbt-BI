from airflow import DAG
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import get_current_context
import requests
from datetime import datetime

# Helper function to get the logical date
def get_logical_date():
    """
    Get the current logical date for the DAG run (Airflow context).
    """
    context = get_current_context()
    return str(context['logical_date'])[:10]

# Helper function to return Snowflake connection
def return_snowflake_conn():
    """
    Return Snowflake connection cursor using SnowflakeHook.
    """
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
    conn = hook.get_conn()
    return conn.cursor()

# Fetch historical population data from World Bank API
@task
def fetch_population_data(start_year, end_year):
    """
    Fetch population data from World Bank API for a given range of years.
    """
    # Construct date range query
    date_range = f"{start_year}:{end_year}"
    api_url = f"https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&date={date_range}&per_page=100"
    population_data = []

    # First request to get the total number of pages
    response = requests.get(f"{api_url}&page=1")

    if response.status_code == 200:
        data = response.json()
        total_pages = data[0].get("pages", 1)  # Get total number of pages

        # Iterate through all the pages using a for loop
        for page in range(1, total_pages + 1):
            page_response = requests.get(f"{api_url}&page={page}")

            if page_response.status_code == 200:
                page_data = page_response.json()

                if len(page_data) > 1 and page_data[1]:
                    records = page_data[1]
                    for record in records:
                        country = record.get("country", {}).get("value", "Unknown")
                        population = record.get("value", None)

                        # Add record to the list
                        population_data.append({
                            "country": country,
                            "year": record.get("date"),
                            "population": population
                        })
                else:
                    print(f"No data found for page {page} of years {start_year} to {end_year}.")
            else:
                print(f"Failed to fetch data for page {page} of years {start_year} to {end_year}. Status code: {page_response.status_code}")
                break  # Exit if there is an issue with fetching data for this page

        print(f"Fetched {len(population_data)} records for the date range {start_year}-{end_year}.")
        return population_data
    else:
        print(f"Failed to fetch data for years {start_year}-{end_year}. Status code: {response.status_code}")
        return []

# Load the population data into Snowflake
@task
def load_population_data(population_data, target_table):
    """
    Load the population data into Snowflake.
    """
    date = get_logical_date()
    cur = return_snowflake_conn()

    try:
        # Create the table in Snowflake if it does not exist
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {target_table} (
            country VARCHAR, year INT, population BIGINT
        )""")

        cur.execute("BEGIN;")

        # Insert or update each record into Snowflake table using MERGE
        for record in population_data:
            sql = f"""
            MERGE INTO {target_table} AS target
            USING (SELECT %s AS country, %s AS year, %s AS population) AS source
            ON target.country = source.country AND target.year = source.year
            WHEN MATCHED THEN
                UPDATE SET population = source.population
            WHEN NOT MATCHED THEN
                INSERT (country, year, population) VALUES (source.country, source.year, source.population);
            """
            cur.execute(sql, (record['country'], record['year'], record['population']))

        # Commit transaction after successful insertions
        cur.execute("COMMIT;")
        print(f"Successfully loaded {len(population_data)} rows into {target_table}")

    except Exception as e:
        # Rollback transaction in case of error
        cur.execute("ROLLBACK;")
        print(f"Error loading data: {e}")
        raise e
    finally:
        # Ensure the cursor is closed after execution
        cur.close()

# Define the DAG
with DAG(
    dag_id='PopulationDataToSnowflake',
    start_date=datetime(2024, 10, 2),
    catchup=False,
    tags=['ETL'],
    schedule_interval='30 2 * * *'  # Run every day at 2:30 AM
) as dag:

    target_table = "dev.raw_data.population_data"

    # Define the date range to fetch (e.g., 2020 to 2023)
    start_year = 2020
    end_year = 2023

    # Fetch population data for the date range
    population_data = fetch_population_data(start_year, end_year)

    # Load the data into Snowflake
    load_population_data(population_data, target_table)
