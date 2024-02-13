import requests

def fetch_currency_data(currencies: list):
    rows = []
    for currency in currencies:
        response = requests.get(f'https://api.coincap.io/v2/rates/{currency}')
        if response.status_code ==200:
            data = response.json()
            data = data['data']

            rows.append(data)
        else:
            rows.append([currency, None, None, None, None])
    return rows
         