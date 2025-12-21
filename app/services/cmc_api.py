import requests
from typing import List, Dict
from app.utils.utils import split_list
import tempfile
import requests_cache
import json

class CoinMarketCapAPI():
    DEFAULT_TIMEOUT = 60
    DEFAULT_BASE_URL = 'https://pro-api.coinmarketcap.com/v2'
    TEMPDIR_CACHE = True
    _session = None

    def __init__(self, api_key=None, request_timeout=DEFAULT_TIMEOUT, base_url=DEFAULT_BASE_URL, tempdir_cache = TEMPDIR_CACHE):
        self.api_key = api_key
        self.base_url = base_url
        self.request_timeout = request_timeout
        self.cache_filename = 'coinmarketcap_cache'
        self.cache_name = os.path.join(tempfile.gettempdir(), self.cache_filename) if tempdir_cache else self.cache_filename
        self.token_prices: Dict[str, float] = {}

    @property
    def session(self):
        if not self._session:
            self._session = requests_cache.CachedSession(cache_name=self.cache_name, backend='sqlite', expire_after=120)
            self._session.headers.update({'Content-Type': 'application/json'})
            self._session.headers.update({'X-CMC_PRO_API_KEY': self.api_key,})
            self._session.headers.update({'Accept': 'application/json'})
            self._session.headers.update({'User-agent': 'crypto-snapshot - python wrapper around CoinMarketCap.com API (github.com/mturnbo/crypto-snapshot)'})
        return self._session

    def make_request(self, endpoint, params):
        url = self.base_url + endpoint
        # print(f"Making request to {url}")
        # print(self.session.headers)

        response_object = self.session.get(url, params=params, timeout=self.request_timeout)

        try:
            response = json.loads(response_object.text)

            if isinstance(response, list) and response_object.status_code == 200:
                response = [dict(item, **{u'cached': response_object.from_cache}) for item in response]
            if isinstance(response, dict) and response_object.status_code == 200:
                response[u'cached'] = response_object.from_cache

        except Exception as e:
            return e

        return response


    def get_token_price(self, symbol: str, currency: str = "USD") -> float:
        params = {
            'symbol': symbol,
            'convert': currency,
        }

        response = self.make_request('/cryptocurrency/quotes/latest', params)

        return response['data'][symbol][0]['quote'][currency]['price']


    def get_token_prices(self, symbols: List, currency: str = "USD") -> Dict[str, float]:
        self.token_prices = {}
        try:
            symbol_groups = split_list(symbols, 40)
            for group in symbol_groups:
                params = {
                    'symbol': ','.join(group),
                    'convert': currency,
                }

                response = self.make_request('/cryptocurrency/quotes/latest', params)
                token_prices: Dict[str, float] = {}
                for symbol in symbols:
                    if symbol in response['data']:
                        symbol_data = response['data'][symbol]
                        if isinstance(symbol_data, list):
                            symbol_data = symbol_data[0]
                        token_prices[symbol] = symbol_data['quote']['USD']['price']

                return token_prices

        except requests.exceptions.RequestException as e:
            print(f"Error fetching from CoinMarketCap: {e}")
            return {}

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_CMC')
cmc = CoinMarketCapAPI(api_key)
token_price = cmc.get_token_price('BTC', 'USD')
print(token_price)

symbols = ['BTC','ETH','ADA']
token_prices = cmc.get_token_prices(symbols)
print(token_prices)
