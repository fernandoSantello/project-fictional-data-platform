import requests

class API:
    def __init__(self):
        self.url_rates = 'https://api.coincap.io/v2/rates/'

    def fetch_currency_data(self, currencies: list):
        rows = []
        for currency in currencies:
            response = requests.get(f'{self.url_rates}{currency}')
            if response.status_code ==200:
                data = response.json()
                data = data['data']

                rows.append(data)
            else:
                rows.append([currency, None, None, None, None])
        return rows
         