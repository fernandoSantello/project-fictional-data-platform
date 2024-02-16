FROM apache/airflow:2.8.1

COPY /dags ./dags
COPY requirements.txt .

RUN pip install -r requirements.txt

USER airflow
