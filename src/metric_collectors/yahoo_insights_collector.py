import asyncio
import json
from typing import List

from metric_publisher.metric_collector import MetricEntry, MetricCollector
from yahoo_finance_api.generated.api.api.insights import asyncio_detailed
from yahoo_finance_api.yahoo_api_source import YahooApiSource, ParseYahooResponseException


class YahooInsightsCollector(YahooApiSource, MetricCollector):
    MEASURE_NAME = "insight"

    async def task(self, symbol: str, mutable_results: List[MetricEntry]):
        raw_res = await asyncio_detailed(client=self.client, symbol=symbol)
        res = json.loads(raw_res.content.decode())
        if 'finance' in res and 'result' in res['finance']:
            finance = res['finance']['result']
        else:
            raise ParseYahooResponseException('stock details response returned an unexpected response')

        mutable_results.append(MetricEntry(
            measure_name=self.MEASURE_NAME,
            tags={"symbol": symbol},
            data=finance
        ))

    async def get_metrics(self) -> List[MetricEntry]:
        result: List[MetricEntry] = []
        tasks = []
        for task_symbol in self.symbols:
            tasks.append(self.task(task_symbol, result))
        await asyncio.gather(*tasks)
        return result
