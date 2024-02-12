import mysql.connector
from datetime import datetime as dt
from api import fetch_currency_data

class MysqlDatabase:
    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.conn = mysql.connector.connect(user=user, 
                                      password=password,
                                      host=host,
                                      database=dbname)
        self.cursor = self.conn.cursor()


    def __enter__(self):
        now = dt.now().strftime('%Y-%m-%d %H:%M:%S')      
        return self, now

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
    def select_statment(self, table_name: str, condition: bool, clause: str = None):
            if not condition:
                self.cursor.execute(f"SELECT * FROM {table_name}")
                rows = self.cursor.fetchall()
            else:
                self.cursor.execute(f"SELECT * FROM {table_name} WHERE {clause}")
                rows = self.cursor.fetchall()               
            return rows
    
    def insert_statment(self, table_name: str, column_values: list):
        sql = f'INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s)'
        print(sql, column_values)
        self.cursor.execute(sql, column_values)


    def delete_statment(self, table_name: str, condition: bool, clause: str = None):
        if not condition:
            sql_query = f"DELETE FROM {table_name}"
            self.cursor.execute(sql_query) 
        else:           
            sql_query = f"DELETE FROM {table_name} WHERE {clause}"
            self.cursor.execute(sql_query)

    def insert_currency_data(self, data):
        with self.conn as (database, now):
            for row in data:
                values = [row.get('id'), row.get('symbol'), row.get('currencySymbol'), row.get('type'), row.get('rateUsd')]
                database.insert_statment('currency', values)            


def main():
    with MysqlDatabase(dbname='teste', user='user', password='user', host='127.0.0.1') as (database, now):
        data = fetch_currency_data(['bitcoin', 'ethereum'])
        for row in data:
            values = [row.get('id'), row.get('symbol'), row.get('currencySymbol'), row.get('type'), row.get('rateUsd')]
            database.insert_statment('currency', values)


if __name__ == '__main__':
    main()
