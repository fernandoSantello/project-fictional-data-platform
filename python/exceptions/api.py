class APIException(Exception):
    def __init__(self, message: str = "Failed to connect with the API"):
        self.message = message
        super().__init__(self.message)

class UnexpectedStatusCodeException(APIException):
    def __init__(self, message: str = "The status code recieved from de API was not 200."):
        self.message = message
        super().__init__(self.message)