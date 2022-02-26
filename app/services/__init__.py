import request
from utils import format_string_with_dict


class BaseService:

    def __init__(self, base_url, **kwargs):
        self._base_url = base_url
        self._headers = kwargs.get('headers')

    def _get(self, endpoint, values=None: dict):
        endpoint = format_string_with_dict(endpoint, values)
        url = self._base_url + endpoint
        response = request.get(url, headers=self._headers)
        return response.json()


