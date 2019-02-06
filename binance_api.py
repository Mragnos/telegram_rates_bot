import time
import urllib
import hmac
import hashlib
import requests
from urllib.parse import urlparse


class Binance:
    methods = {
        'ping': {'url': 'api/v1/ping', 'method': 'GET', 'private': False},
        'time': {'url': 'api/v1/time', 'method': 'GET', 'private': False},
        'exchangeInfo': {'url': 'api/v1/exchangeInfo', 'method': 'GET', 'private': False},
        'depth': {'url': 'api/v1/depth', 'method': 'GET', 'private': False},
        'trades': {'url': 'api/v1/trades', 'method': 'GET', 'private': False},
        'historicalTrades': {'url': 'api/v1/historicalTrades', 'method': 'GET', 'private': False},
        'aggTrades': {'url': 'api/v1/aggTrades', 'method': 'GET', 'private': False},
        'klines': {'url': 'api/v1/klines', 'method': 'GET', 'private': False},
        'ticker24hr': {'url': 'api/v1/ticker/24hr', 'method': 'GET', 'private': False},
        'tickerPrice': {'url': 'api/v3/ticker/price', 'method': 'GET', 'private': False},
        'tickerBookTicker': {'url': 'api/v3/ticker/bookTicker', 'method': 'GET', 'private': False}
    }

    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = bytearray(API_SECRET, encoding='utf-8')
        self.shift_seconds = 0

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            kwargs.update(command=name)
            return self.call_api(**kwargs)

        return wrapper

    def call_api(self, **kwargs):

        command = kwargs.pop('command')
        api_url = 'https://api.binance.com/' + self.methods[command]['url']

        payload = kwargs
        headers = {}

        payload_str = urllib.parse.urlencode(payload)
        if self.methods[command]['private']:
            payload.update({'timestamp': int(time.time() + self.shift_seconds - 1) * 1000})
            payload_str = urllib.parse.urlencode(payload).encode('utf-8')
            sign = hmac.new(
                key=self.API_SECRET,
                msg=payload_str,
                digestmod=hashlib.sha256
            ).hexdigest()

            payload_str = payload_str.decode("utf-8") + "&signature=" + str(sign)
            headers = {"X-MBX-APIKEY": self.API_KEY}

        if self.methods[command]['method'] == 'GET':
            api_url += '?' + payload_str

        response = requests.request(method=self.methods[command]['method'], url=api_url,
                                    data="" if self.methods[command]['method'] == 'GET' else payload_str,
                                    headers=headers)
        if 'code' in response.text:
            print(response.text)
        return response.json()
