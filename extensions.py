import json
import requests
from requests import HTTPError, Timeout, ConnectionError
from config import *


class APIException(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Ошибка в написании валюты {base}.\n'
                               f'Список поддерживаемых валют можно посмотреть командой /values')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Ошибка в написании валюты {quote}.\n'
                               f'Список поддерживаемых валют можно посмотреть командой /values')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f'Ошибка количества валюты {amount}.\nПоддерживаются только целочисленные значения')

        try:
            request = requests.get(
                f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}', timeout=2)
        except (HTTPError, Timeout, ConnectionError):
            raise Exception(f'\nОшибка доступа к сайту с курсом валют.\nПовторите запрос позже.')

        total_quote = float(json.loads(request.content)[keys[quote]])*amount
        return total_quote
