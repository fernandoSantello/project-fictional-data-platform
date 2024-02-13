from dotenv import load_dotenv
import os
import mysql.connector
from datetime import datetime as dt
from .exceptions.exceptions import DatabaseException, InsertException, SelectException

load_dotenv()
class MysqlDatabase:
    def __init__(self):
        self.conn = mysql.connector.connect(user=os.getenv('DB_CURRENCY_DATA_USER'), 
                                      password=os.getenv('DB_CURRENCY_DATA_PASSWORD'),
                                      host=os.getenv('DB_CURRENCY_DATA_HOST'),
                                      database=os.getenv('DB_CURRENCY_DATA_NAME'))
        self.cursor = self.conn.cursor()


    def __enter__(self):
        now = dt.now().strftime('%Y-%m-%d %H:%M:%S')      
        return self, self.cursor, now


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        

    def select_statment(self, table_name: str, condition: bool, clause: str = None) -> list:
            with MysqlDatabase() as (dbobject, cursor, now):
                try:
                    if condition:
                        cursor.execute(f"SELECT * FROM {table_name} WHERE {clause}")
                        rows = cursor.fetchall() 
                    else:
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()             
                    return rows
                except:
                    raise SelectException
    

    def insert_statment(self, table_name: str, column_values: dict) -> None:
        with MysqlDatabase() as (dbobject, cursor, now):
            column_values['timestamp'] = now
            placeholders = ','.join(['%s' for _ in range(len(column_values))])
            column_names =  dbobject.get_column_names(table_name=table_name)
            sql = f'INSERT INTO {table_name} {column_names} VALUES ({placeholders})'
            sql = sql.replace('[', '(').replace(']', ')').replace("'", '')
            try:
                cursor.execute(sql, list(column_values.values()))
            except:
                raise InsertException


    def get_column_names(self, table_name: str) -> list:
        with MysqlDatabase() as (dbobject, cursor, now):
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]
            columns = columns[1::]
            return columns


    def delete_statment(self, table_name: str, condition: bool, clause: str = None) -> None:
        with MysqlDatabase() as (dbobject, cursor, now):
            if condition:
                sql_query = f"DELETE FROM {table_name} WHERE {clause}"
                cursor.cursor.execute(sql_query)
            else:
                sql_query = f"DELETE FROM {table_name}"
                cursor.cursor.execute(sql_query)


    def check_currency(self, currency: str) -> bool:
        row = self.select_statment(table_name='currency', condition=1, clause=f'name = "{currency}" LIMIT 1')
        return bool(row)
    

    def get_id_currency(self, currency: str) -> int:

        row = self.select_statment(table_name='currency', condition=1,
                                        clause=f'name = "{currency}" LIMIT 1')
        return row[0][0]


    def insert_currency_data(self, data: list) -> None:
        for row in data:
            values = [row.get('id'), row.get('symbol'),
                        row.get('currencySymbol'), row.get('type'), row.get('rateUsd')]
            self.insert_statment(table_name='currency',column_values=values)
