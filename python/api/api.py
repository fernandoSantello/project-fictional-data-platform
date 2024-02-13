import requests
from .exceptions.exceptions import ApiException, NotExceptedResponseException

class API:
    def __init__(self):
        self.url_rates = 'https://api.coincap.io/v2/rates/'

    def fetch_currency_data(self, currency: str) -> dict:
        response = requests.get(f'{self.url_rates}{currency}')
        if response.status_code == 200:
            data = response.json()
            data = data['data']
            return data
        else:
            raise NotExceptedResponseException
            