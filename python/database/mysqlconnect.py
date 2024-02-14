from dotenv import load_dotenv
import os
import mysql.connector
from datetime import datetime as dt
from .exceptions.exceptions import DatabaseException, InsertException, SelectException

load_dotenv()
class MysqlDatabase:
    def __init__(self):
        self.conn = mysql.connector.connect(user=os.getenv('DB_CURRENCY_DATA_USER_CONTAINER'), 
                                      password=os.getenv('DB_CURRENCY_DATA_PASSWORD'),
                                      host=os.getenv('DB_CURRENCY_DATA_HOST'),
                                      database=os.getenv('DB_CURRENCY_DATA_NAME'))
        self.cursor = self.conn.cursor()


    def __enter__(self):
        now = dt.now().strftime('%Y-%m-%d %H:%M:%S')      
        return self, self.cursor, now


    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.conn.commit()
        except mysql.connector.Error as e:
            raise DatabaseException(f"Database commit error: {e}")
        finally:
            self.cursor.close()
            self.conn.close()
        

    def select_statement(self, table_name: str, condition: bool, clause: str = None) -> list:
            with MysqlDatabase() as (dbobject, cursor, now):
                try:
                    if condition:
                        cursor.execute(f"SELECT * FROM {table_name} WHERE {clause}") 
                    else:
                        cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()             
                    return rows
                except mysql.connector.Error as e:
                    raise SelectException(f'Error executing SELECT statement: {e}')
    

    def insert_statement(self, table_name: str, column_values: dict) -> None:
        with MysqlDatabase() as (dbobject, cursor, now):
            column_values['timestamp'] = now
            placeholders = ','.join(['%s' for _ in range(len(column_values))])
            column_names =  dbobject.get_column_names(table_name=table_name)
            sql = f'INSERT INTO {table_name} {column_names} VALUES ({placeholders})'
            sql = sql.replace('[', '(').replace(']', ')').replace("'", '')
            try:
                cursor.execute(sql, list(column_values.values()))
            except mysql.connector.Error as e:
                raise InsertException(f'Error executing INSERT statement: {e}')


    def get_column_names(self, table_name: str) -> list:
        with MysqlDatabase() as (dbobject, cursor, now):
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]
            columns = columns[1::]
            return columns


    def check_currency(self, currency: str) -> bool:
        row = self.select_statement(table_name='currency', condition=1, clause=f'name = "{currency}" LIMIT 1')
        return bool(row)
    

    def get_id_currency(self, currency: str) -> int:
        row = self.select_statement(table_name='currency', condition=1,
                                        clause=f'name = "{currency}" LIMIT 1')
        return row[0][0]
