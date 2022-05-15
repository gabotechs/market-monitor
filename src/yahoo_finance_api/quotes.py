import pydantic
import json
from typing import Optional, List, Dict

from .generated.api.api.quotes import asyncio_detailed
from .yahoo_api_source import YahooApiSource, ParseYahooResponseException


class SymbolQuote(pydantic.BaseModel):
    language: Optional[str]
    region: Optional[str]
    quoteType: Optional[str]
    typeDisp: Optional[str]
    quoteSourceName: Optional[str]
    triggerable: Optional[bool]
    customPriceAlertConfidence: Optional[str]
    currency: Optional[str]
    tradeable: Optional[bool]
    exchange: Optional[str]
    shortName: Optional[str]
    longName: Optional[str]
    messageBoardId: Optional[str]
    exchangeTimezoneName: Optional[str]
    exchangeTimezoneShortName: Optional[str]
    gmtOffSetMilliseconds: Optional[int]
    market: Optional[str]
    esgPopulated: Optional[bool]
    firstTradeDateMilliseconds: Optional[int]
    priceHint: Optional[int]
    regularMarketChange: Optional[float]
    regularMarketChangePercent: Optional[float]
    regularMarketTime: Optional[int]
    regularMarketPrice: Optional[float]
    regularMarketDayHigh: Optional[float]
    regularMarketDayRange: Optional[str]
    regularMarketDayLow: Optional[float]
    regularMarketVolume: Optional[int]
    regularMarketPreviousClose: Optional[float]
    bid: Optional[float]
    ask: Optional[float]
    bidSize: Optional[int]
    askSize: Optional[int]
    fullExchangeName: Optional[str]
    financialCurrency: Optional[str]
    regularMarketOpen: Optional[float]
    averageDailyVolume3Month: Optional[int]
    averageDailyVolume10Day: Optional[int]
    fiftyTwoWeekLowChange: Optional[float]
    fiftyTwoWeekLowChangePercent: Optional[float]
    fiftyTwoWeekRange: Optional[str]
    fiftyTwoWeekHighChange: Optional[float]
    fiftyTwoWeekHighChangePercent: Optional[float]
    fiftyTwoWeekLow: Optional[float]
    fiftyTwoWeekHigh: Optional[float]
    dividendDate: Optional[int]
    earningsTimestamp: Optional[int]
    earningsTimestampStart: Optional[int]
    earningsTimestampEnd: Optional[int]
    trailingAnnualDividendRate: Optional[float]
    trailingPE: Optional[float]
    trailingAnnualDividendYield: Optional[float]
    epsTrailingTwelveMonths: Optional[float]
    epsForward: Optional[float]
    epsCurrentYear: Optional[float]
    priceEpsCurrentYear: Optional[float]
    sharesOutstanding: Optional[int]
    bookValue: Optional[float]
    fiftyDayAverage: Optional[float]
    fiftyDayAverageChange: Optional[float]
    fiftyDayAverageChangePercent: Optional[float]
    twoHundredDayAverage: Optional[float]
    twoHundredDayAverageChange: Optional[float]
    twoHundredDayAverageChangePercent: Optional[float]
    marketCap: Optional[int]
    forwardPE: Optional[float]
    priceToBook: Optional[float]
    sourceInterval: Optional[int]
    exchangeDataDelayedBy: Optional[int]
    pageViewGrowthWeekly: Optional[float]
    averageAnalystRating: Optional[str]
    marketState: Optional[str]
    displayName: Optional[str]
    symbol: Optional[str]


class QuoteSource(YahooApiSource[SymbolQuote]):
    async def retrieve(self, symbols: List[str]) -> Dict[str, SymbolQuote]:
        raw_res = await asyncio_detailed(client=self.client, symbols=','.join(symbols))
        res = json.loads(raw_res.content.decode())
        if 'quoteResponse' not in res or 'result' not in res['quoteResponse']:
            raise ParseYahooResponseException('badly formed quote response:\n'+json.dumps(res, indent=4))

        result: Dict[str, SymbolQuote] = {}
        for raw_quote in res['quoteResponse']['result']:
            if 'symbol' not in raw_quote:
                raise ParseYahooResponseException('got one quote without symbol:\n' + json.dumps(raw_quote, indent=4))
            result[raw_quote["symbol"]] = SymbolQuote(**raw_quote)

        return result
