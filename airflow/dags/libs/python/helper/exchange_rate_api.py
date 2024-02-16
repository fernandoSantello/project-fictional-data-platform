from libs.python.services.exchange_rate_api import ExchangeRateConnection

class ExchangeRateAPI:
    def __init__(self, conn_param: dict):
        self.conn_param = conn_param
        self.conn_api = ExchangeRateConnection(conn_param=conn_param)

    
    def get_rates(self) -> dict:
        response = self.conn_api.get_request(f'/latest/USD')
        if response.status_code == 200:
            data = response.json()
            data = data['conversion_rates']
            return data
        else: 
            print(response.status_code)
            