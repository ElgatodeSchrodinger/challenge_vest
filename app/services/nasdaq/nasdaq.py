from services import BaseService


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
        return self._get(url_format, {'symbol': symbol}).get('data')
