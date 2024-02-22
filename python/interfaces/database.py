from abc import ABC, abstractmethod
from typing import Union

class Database(ABC):
    
    @abstractmethod
    def insert_statement(self, sql: tuple) -> None:
        pass


    @abstractmethod
    def delete_statement(self, sql: tuple) -> None:
        pass


    @abstractmethod
    def update_statement(self, sql: tuple) -> None:
        pass


    @abstractmethod
    def select_statement(self, sql: tuple, fetch_single: bool) -> Union[list, bool, None]:
        pass
