from helper.coincap_api import CoincapAPI
from helper.exchange_rate_api import ExchangeRateAPI
from helper.mysql_db import DBMysql
from helper.postgres_db import DBPostgres
from helper.dataframe_operator import tuple_to_dataframe, create_multiplied_column, concatenate_dataframes
from typing import Union
from dotenv import load_dotenv
import os

class Controller:
    def __init__(self):
        load_dotenv()
        self.db_mysql = DBMysql(conn_param={
            'user': os.getenv('MYSQL_PROD_USER'),
            'password': os.getenv('MYSQL_PROD_PASSWORD'),
            'host': os.getenv('MYSQL_PROD_HOST'),
            'database': os.getenv('MYSQL_PROD_DATABASE'),
            'database_type': 'mysql'
        })
        self.db_postgres = DBPostgres(conn_param={
            'user': os.getenv('POSTGRES_PROD_USER'),
            'password': os.getenv('POSTGRES_PROD_PASSWORD'),
            'host': os.getenv('POSTGRES_PROD_HOST'),
            'database': os.getenv('POSTGRES_PROD_DATABASE'),
            'database_type': 'postgres'
        })
        self.api_coincap = CoincapAPI(conn_param={
            'url': os.getenv('COINCAP_API_URL'),
            'api_key': os.getenv('COINCAP_API_KEY')
        })
        self.api_exchangerate = ExchangeRateAPI(conn_param={
            'url': os.getenv('EXCHANGERATE_API_URL'),
            'api_key': os.getenv('EXCHANGERATE_API_KEY')
        })
        self.currencies = ['bitcoin', 'ethereum']

    
    def get_currency_info(self, currency: str) -> Union[bool, dict]:
        currency_data = self.api_coincap.get_rates(currency=currency)
        check = self.db_mysql.check_currency(currency_data['id'])
        return (True, currency_data) if check else (False, currency_data)
    

    def insert_rate(self, currency_data: dict) -> None:
        id_currency = self.db_mysql.get_id_currency(currency=currency_data['id'])
        row_values = {
            'id_currency': id_currency,
            'rateUsd': currency_data['rateUsd']
        }
        self.db_mysql.insert_rate(row_values=row_values)


    def insert_currency(self, currency_data: dict) -> None:
        row_values = {
            'name': currency_data['id'],
            'symbol': currency_data['symbol'],
            'currencySymbol': currency_data['currencySymbol'],
            'type': currency_data['type']
        }
        self.db_mysql.insert_currency(row_values=row_values)


    def sync_currency_data(self) -> None:
        for element in self.currencies:
            curency_exists, currency_data = self.get_currency_info(element)
            self.insert_rate(currency_data) if curency_exists else self.insert_currency(currency_data)


    def get_currency_mysql(self) -> list:
        postgres_last_id = self.db_postgres.get_lat_id_currency()
        rows = self.db_mysql.get_currency_table(postgres_last_id=postgres_last_id)
        return rows


    def get_rate_mysql(self) -> list:
        postgres_last_id = self.db_postgres.get_lat_id_rate()
        rows = self.db_mysql.get_rate_table(postgres_last_id=postgres_last_id)
        return rows
    

    def get_process_fail_mysql(self) -> list:
        postgres_last_id = self.db_postgres.get_lat_id_process_fail()
        rows = self.db_mysql.get_process_fail_table(postgres_last_id=postgres_last_id)
        return rows


    def treat_data(self):
        currency_table = tuple_to_dataframe(self.get_currency_mysql())
        #rating_table = tuple_to_dataframe(self.get_rate_mysql())
        #process_fail_table = tuple_to_dataframe(self.get_process_fail_mysql())
        print(currency_table)
        