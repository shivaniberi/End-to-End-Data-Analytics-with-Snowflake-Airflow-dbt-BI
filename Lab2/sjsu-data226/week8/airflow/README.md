## How to Run Airflow via Docker Compose With Celery Executor

1. Clone the repo to your computer
```
git clone https://github.com/keeyong/sjsu-data226.git
```
2. Change the current directory to sjsu-data226/week8/airflow
```
cd sjsu-data226/week8/airflow
```
3. First initialize Airflow environment
```
docker compose up airflow-init
```
4. Next run the Airflow service
```
docker compose up
```
5. Wait some time, then visit http://localhost:8080 and log in (Use ID:PW of airflow:airflow)
