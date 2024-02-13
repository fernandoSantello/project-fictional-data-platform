class DatabaseException(Exception):
    def __init__(self, message: str = "Could not connect to the Database"):
        self.message = message

        super().__init__(self.message)


class InsertException(DatabaseException):

    def __init__(self):
        super().__init__(message="Failed to execute INSERT statement")

class SelectException(DatabaseException):

    def __init__(self):
        super().__init__(message="Failed to execute SELECT statement")