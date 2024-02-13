class ApiException(Exception):
    def __init__(self, message: str = "API Fail"):
        self.message = message

        super().__init__(self.message)

class NotExceptedResponseException(ApiException):

    def __init__(self):
        super().__init__(message="Unexpected response from server")
