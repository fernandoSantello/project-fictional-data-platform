class DatabaseException(Exception):
    def __init__(self, message: str = "Failed to connect with the Database"):
        self.message = message
        super().__init__(self.message)

class StatementException(DatabaseException):
    def __init__(self, message: str = "Failed to correctly execute provided statement."):
        self.message = message
        super().__init__(self.message)
