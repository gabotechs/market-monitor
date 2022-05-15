from abc import ABC, abstractmethod
from typing import List, Dict, Generic, TypeVar
from .generated import Client


class ParseYahooResponseException(Exception):
    pass


T = TypeVar('T')


class YahooApiSource(ABC, Generic[T]):
    def __init__(self, url: str = 'https://query1.finance.yahoo.com'):
        self.client = Client(url, timeout=10, verify_ssl=True)

    @abstractmethod
    async def retrieve(self, symbols: List[str]) -> Dict[str, T]:
        raise NotImplementedError()
