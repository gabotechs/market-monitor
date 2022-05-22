from typing import List
from logging import Logger

from .generated import Client


class ParseYahooResponseException(Exception):
    pass


class YahooApiSource:
    def __init__(self,
                 symbols: List[str],
                 logger: Logger,
                 url: str = 'https://query1.finance.yahoo.com'):
        self.logger = logger
        self.client = Client(url, timeout=10, verify_ssl=True)
        self.symbols = symbols
