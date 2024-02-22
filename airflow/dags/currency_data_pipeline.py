import os
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
from dotenv import load_dotenv, find_dotenv
from python.controller.controller import Controller
from python.helper.coincap_api import CoincapAPI
from python.services.coincap_api import CoincapConnection
from python.helper.exchange_rate_api import ExchangeRateAPI
from python.services.exchange_rate_api import ExchangeRateConnection
from python.helper.mysql_db import DBMysql
from python.services.mysql_db import MysqlDBConnection
from python.helper.postgres_db import DBPostgres
from python.services.postgress_db import PostgresDBConnection


load_dotenv(find_dotenv())


postgres_db = DBPostgres(conn_db=PostgresDBConnection(conn_param={
            'user': os.getenv('POSTGRES_PROD_USER'),
            'password': os.getenv('POSTGRES_PROD_PASSWORD'),
            'host': os.getenv('POSTGRES_PROD_HOST'),
            'database': os.getenv('POSTGRES_PROD_DATABASE'),
            'database_type': 'postgres'
        }))


mysql_db = DBMysql(conn_db=MysqlDBConnection(conn_param={
            'user': os.getenv('MYSQL_PROD_USER'),
            'password': os.getenv('MYSQL_PROD_PASSWORD'),
            'host': os.getenv('MYSQL_PROD_HOST'),
            'database': os.getenv('MYSQL_PROD_DATABASE'),
        }))


api_exchangerate = ExchangeRateAPI(conn_api=ExchangeRateConnection(conn_param={
            'url': os.getenv('EXCHANGERATE_API_URL'),
            'api_key': os.getenv('EXCHANGERATE_API_KEY')
        }))


api_coincap = CoincapAPI(conn_api=CoincapConnection(conn_param={
            'url': os.getenv('COINCAP_API_URL'),
            'api_key': os.getenv('COINCAP_API_KEY')
            }))


rds_postgres_db = DBPostgres(conn_db=PostgresDBConnection(conn_param={
            'user': os.getenv('RDS_USARNAME'),
            'password': os.getenv('RDS_PASSWORD'),
            'host': os.getenv('RDS_ENDPOINT'),
            'database': os.getenv('RDS_DATABASE')
        }))


controler_local = Controller(api_rate=api_coincap, api_exchange_rate=api_exchangerate, source_database=mysql_db, target_database=postgres_db)

controler_cloud = Controller(api_rate=api_coincap, api_exchange_rate=api_exchangerate, source_database=postgres_db, target_database=rds_postgres_db)


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'email': ['fersrp1964@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}


@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(0))
def currency_data_pipeline():


    @task()
    def extract_data_from_api():
        controler_local.sync_currency_data()
    

    @task()
    def gather_data_for_local():
        insert_currency_table, insert_rate_table, insert_process_fail_table = controler_local.gather_table_data_from_source(treat_data=True)
        tables = {
            'insert_currency_table': insert_currency_table,
            'insert_rate_table': insert_rate_table,
            'insert_process_fail_table': insert_process_fail_table
        }
        return tables
    

    @task()
    def load_data_to_local(tables):
        controler_local.insert_into_target_database(tables['insert_currency_table'], tables['insert_rate_table'], tables['insert_process_fail_table'])


    @task()
    def gather_data_for_cloud():
        insert_currency_table, insert_rate_table, insert_process_fail_table = controler_cloud.gather_table_data_from_source(treat_data=False)
        tables = {
            'insert_currency_table': insert_currency_table,
            'insert_rate_table': insert_rate_table,
            'insert_process_fail_table': insert_process_fail_table
        }
        return tables
    
    
    @task()
    def load_data_to_cloud(tables):
        controler_cloud.insert_into_target_database(tables['insert_currency_table'], tables['insert_rate_table'], tables['insert_process_fail_table'])

    
    A = extract_data_from_api()
    B = gather_data_for_local()
    C = load_data_to_local(B)
    D = gather_data_for_cloud()
    E = load_data_to_cloud(D)

    A >> B >> C >> D >> E

    
currency_data_pipeline = currency_data_pipeline()
