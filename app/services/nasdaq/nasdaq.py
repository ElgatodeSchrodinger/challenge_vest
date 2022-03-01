from services import BaseService
from exceptions import ClientException

class NASDAQService(BaseService):

    def __init__(self):
        connection_values = {
            'headers': {
                'user-agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/75.0.3770.142 Safari/537.36'
                    )
            }
        }
        super().__init__('https://api.nasdaq.com/api', connection_values)

    def get_stock_by_symbol(self, symbol: str):
        url_format = '/quote/{symbol}/info?assetclass=stocks'
        response = self._get(url_format, {'symbol': symbol})

        status_code = response.get('status', {}).get('rCode')

        if status_code in (200,):
            return response.get('data')
        elif status_code >= 400:
            message = response \
                .get('status', {}) \
                .get('bCodeMessage')[0] \
                .get('errorMessage')
            raise ClientException(message, status_code)

