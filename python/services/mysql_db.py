import mysql.connector
from datetime import datetime as dt
from typing import Union
from python.interfaces.database import Database
from python.exceptions.database import DatabaseException, StatementException
from mysql.connector.errors import ProgrammingError, DatabaseError

class MysqlDBConnection(Database):
    def __init__(self, conn_param: dict):
        self.conn_param = conn_param
        self.conn = None
        self.cursor = None


    def __enter__(self):
        self.conn = mysql.connector.connect(user=self.conn_param['user'], 
                                    password=self.conn_param['password'],
                                    host=self.conn_param['host'],
                                    database=self.conn_param['database'])
        self.cursor = self.conn.cursor(dictionary=True)
        now = dt.now().strftime('%Y-%m-%d %H:%M:%S')      
        return self, now


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if type(exc_value) == ProgrammingError:
            raise StatementException
        if type(exc_value) == DatabaseError:
            raise DatabaseException
        
    
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
