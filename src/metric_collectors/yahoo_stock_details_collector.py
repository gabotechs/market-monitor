import json
import asyncio
from typing import List

from metric_publisher.metric_collector import MetricEntry, MetricCollector
from yahoo_finance_api.generated.api.api.stock_details import asyncio_detailed
from yahoo_finance_api.yahoo_api_source import YahooApiSource, ParseYahooResponseException

modules = [
    # 'summaryDetail',
    # 'fundProfile',
    'financialData',
    # 'defaultKeyStatistics',
    # 'calendarEvents',
    # 'incomeStatementHistory',
    # 'incomeStatementHistoryQuarterly',
    # 'cashflowStatementHistory',
    # 'balanceSheetHistory',
    # 'earnings',
    # 'earningsHistory',
    # 'insiderHolders',
    # 'cashflowStatementHistory',
    # 'cashflowStatementHistoryQuarterly',
    # 'insiderTransactions',
    # 'secFilings',
    # 'indexTrend',
    # 'sectorTrend',
    # 'earningsTrend',
    # 'netSharePurchaseActivity',
    # 'upgradeDowngradeHistory',
    # 'institutionOwnership',
    'recommendationTrend',
    # 'balanceSheetHistory',
    # 'balanceSheetHistoryQuarterly',
    # 'fundOwnership',
    # 'majorDirectHolders',
    # 'majorHoldersBreakdown',
    # 'price',
    # 'quoteType',
    # 'esgScores'
]


class YahooStockDetailsCollector(YahooApiSource, MetricCollector):
    MEASURE_NAME = "stock_details"
    MEASURE_NAME_2 = "recommendation_trend"

    async def task(self, symbol: str, mutable_result: List[MetricEntry]):
        raw_res = await asyncio_detailed(
            client=self.client,
            symbol=symbol,
            modules=','.join(modules)
        )
        res = json.loads(raw_res.content.decode())
        if 'quoteSummary' in res \
                and 'error' in res['quoteSummary'] \
                and res['quoteSummary']['error']:
            error = res['quoteSummary']['error']
            msg = f'{symbol} {error["code"]}: {error["description"]}'
            if error['code'] == 'Not Found':
                self.logger.warning(msg)
                return
            raise Exception(msg)

        if 'quoteSummary' in res \
                and 'result' in res['quoteSummary'] \
                and len(res['quoteSummary']['result']):
            quote_summary_result = res['quoteSummary']['result'][0]
        else:
            raise ParseYahooResponseException('stock details response returned an unexpected response')

        if 'financialData' in quote_summary_result:
            mutable_result.append(MetricEntry(
                measure_name=self.MEASURE_NAME,
                tags={"symbol": symbol},
                data=quote_summary_result['financialData']
            ))
        if 'recommendationTrend' in quote_summary_result \
                and 'trend' in quote_summary_result['recommendationTrend'] \
                and len(quote_summary_result['recommendationTrend']['trend']):
            mutable_result.append(MetricEntry(
                measure_name=self.MEASURE_NAME_2,
                tags={"symbol": symbol},
                data=quote_summary_result['recommendationTrend']['trend'][0]
            ))

    async def get_metrics(self) -> List[MetricEntry]:
        result: List[MetricEntry] = []
        tasks = []
        for task_symbol in self.symbols:
            tasks.append(self.task(task_symbol, result))
        await asyncio.gather(*tasks)
        return result
