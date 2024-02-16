from libs.python.helper.api import API
from libs.python.helper.mysql_db import DBMysql
from libs.python.helper.postgres_db import DBPostgres
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
        self.api = API(conn_param={
            'url': os.getenv('API_URL'),
            'api_key': os.getenv('API_KEY')
        })
        self.currencies = ['bitcoin', 'ethereum']

    
    def get_currency_info(self, currency: str) -> Union[bool, dict]:
        currency_data = self.api.get_rates(currency=currency)
        check = self.db_mysql.check_currency(currency_data['id'])
        if check:
            return True, currency_data
        else:
            return False, currency_data
    

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


    def execution_process(self) -> None:
        for element in self.currencies:
            curency_exists, currency_data = self.get_currency_info(element)
            if curency_exists:
                self.insert_rate(currency_data=currency_data)
            else:
                self.insert_currency(currency_data=currency_data)
