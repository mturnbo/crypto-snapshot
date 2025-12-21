import os
import requests
import requests_cache
import jwt
from typing import Dict, List, Any
import tempfile
import json
import urllib.parse
import hashlib
import hmac
import base64
import time

class BinanceUSAPI():
    DEFAULT_TIMEOUT = 60
    DEFAULT_BASE_URL = 'https://api.binance.us'
    TEMPDIR_CACHE = True
    _session = None

    def __init__(self, api_key: str, api_secret: str, request_timeout=DEFAULT_TIMEOUT, base_url=DEFAULT_BASE_URL, tempdir_cache = TEMPDIR_CACHE):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.request_timeout = request_timeout
        self.cache_filename = 'binanceus_cache'
        self.cache_name = os.path.join(tempfile.gettempdir(), self.cache_filename) if tempdir_cache else self.cache_filename
        self.token_prices: Dict[str, float] = {}

    @property
    def session(self):
        if not self._session:
            self._session = requests_cache.CachedSession(cache_name=self.cache_name, backend='memory', expire_after=120)
            self._session.headers.update({'Content-Type': 'application/json'})
            self._session.headers.update({'X-MBX-APIKEY': self.api_key })
            self._session.headers.update({'Accept': 'application/json'})
            self._session.headers.update({'User-agent': 'crypto-snapshot - python wrapper around BinanceUS.com API (github.com/mturnbo/crypto-snapshot)'})
        return self._session

    def get_binanceus_signature(self, data):
        postdata = urllib.parse.urlencode(data)
        message = postdata.encode()
        byte_key = bytes(self._apisecret, 'UTF-8')
        mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return mac

    def make_request(self, endpoint,params):
        # headers = {}
        # headers['X-MBX-APIKEY'] = self.api_key
        # signature = self.get_binanceus_signature(endpoint_params)
        # params = {
        #     **endpoint_params,
        #     "signature": signature,
        # }
        # req = requests.get((self.base_url + endpoint), params=params, headers=headers)
        #
        # return req.text

        url = self.base_url + endpoint
        signature = self.get_binanceus_signature(params)
        params['signature'] = signature

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
