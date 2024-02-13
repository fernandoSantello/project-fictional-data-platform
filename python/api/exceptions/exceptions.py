class ApiException(Exception):
    def __init__(self, message: str = "Falha na API"):
        self.message = message

        super().__init__(self.message)

class NotExceptedResponseException(ApiException):

    def __init__(self):
        super().__init__(message="Código de resposta inesperado")
