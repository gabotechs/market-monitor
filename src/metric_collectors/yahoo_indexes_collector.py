import json
import logging
from typing import List

from metric_publisher.metric_collector import MetricCollector, MetricEntry
from yahoo_finance_api.generated.api.api.quotes import asyncio_detailed
from yahoo_finance_api.yahoo_api_source import YahooApiSource, ParseYahooResponseException


class YahooIndexesCollector(YahooApiSource, MetricCollector):
    MEASURE_NAME = "indexes"
    INDEXES = [
        "^GSPC",
        "^DJI",
        "^IXIC",
        "^VIX"
    ]

    def __init__(self, logger: logging.Logger):
        super(YahooIndexesCollector, self).__init__(self.INDEXES, logger)

    async def get_metrics(self) -> List[MetricEntry]:
        raw_res = await asyncio_detailed(client=self.client, symbols=','.join(self.symbols))
        res = json.loads(raw_res.content.decode())
        if 'quoteResponse' not in res or 'result' not in res['quoteResponse']:
            raise ParseYahooResponseException('badly formed quote response:\n'+json.dumps(res, indent=4))

        result: List[MetricEntry] = []
        for raw_quote in res['quoteResponse']['result']:
            if 'shortName' not in raw_quote:
                raise ParseYahooResponseException('got one quote without shortName:\n' + json.dumps(raw_quote, indent=4))
            result.append(MetricEntry(
                measure_name=self.MEASURE_NAME,
                tags={"index": raw_quote['shortName']},
                data=raw_quote
            ))

        return result
