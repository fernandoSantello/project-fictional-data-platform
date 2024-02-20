import psycopg2
import psycopg2.extras
from datetime import datetime as dt
from typing import Union
from libs.python.interfaces.database import InterfaceDatabase

class PostgresDBConnection(InterfaceDatabase):
    def __init__(self, conn_param: dict):
        self.user = conn_param['user']
        self.password = conn_param['password']
        self.host = conn_param['host']
        self.database = conn_param['database']
        self.conn = None
        self.cursor = None


    def __enter__(self):
        self.conn = psycopg2.connect(
        user=self.user,
        password=self.password,
        host=self.host,
        dbname=self.database
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        now = dt.now().strftime('%Y-%m-%d %H:%M:%S')      
        return self, now


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
    
    def insert_statement(self, sql: tuple) -> None:
        self.cursor.execute(sql[0], sql[1])


    def delete_statement(self, sql: tuple) -> None:
        self.cursor.execute(sql[0], sql[1])

    
    def update_statement(self, sql: tuple) -> None:
        self.cursor.execute(sql[0], sql[1])


    def select_statement(self, sql: tuple, fetch_single: bool) -> Union[list, bool, None]:
        self.cursor.execute(sql[0], sql[1])
        if fetch_single:
            row = self.cursor.fetchone()
        else:
            row = self.cursor.fetchall()
        return row
