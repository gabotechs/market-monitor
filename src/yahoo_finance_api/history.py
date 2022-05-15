import pydantic
import json
from typing import List, Dict

from .generated.api.api.history import asyncio_detailed
from .yahoo_api_source import YahooApiSource


class SymbolHistory(pydantic.BaseModel):
    timestamp: List[int]
    symbol: str
    end: int
    start: int
    previousClose: float
    chartPreviousClose: float
    close: List[float]
    dataGranularity: int


class HistorySource(YahooApiSource[SymbolHistory]):
    async def retrieve(self, symbols: List[str]) -> Dict[str, SymbolHistory]:
        raw_res = await asyncio_detailed(client=self.client, symbols=','.join(symbols))
        res = json.loads(raw_res.content.decode())
        result: Dict[str, SymbolHistory] = {}
        for symbol, entry in res.items():
            result[symbol] = SymbolHistory(**entry)
        return result
