import json
from typing import List

from metric_publisher.metric_collector import MetricEntry, MetricCollector
from yahoo_finance_api.generated.api.api.stock_details import asyncio_detailed
from yahoo_finance_api.yahoo_api_source import YahooApiSource, ParseYahooResponseException

modules = [
    'summaryDetail',
    'fundProfile',
    'financialData',
    'defaultKeyStatistics',
    'calendarEvents',
    'incomeStatementHistory',
    'incomeStatementHistoryQuarterly',
    'cashflowStatementHistory',
    'balanceSheetHistory',
    'earnings',
    'earningsHistory',
    'insiderHolders',
    'cashflowStatementHistory',
    'cashflowStatementHistoryQuarterly',
    'insiderTransactions',
    'secFilings',
    'indexTrend',
    'sectorTrend',
    'earningsTrend',
    'netSharePurchaseActivity',
    'upgradeDowngradeHistory',
    'institutionOwnership',
    'recommendationTrend',
    'balanceSheetHistory',
    'balanceSheetHistoryQuarterly',
    'fundOwnership',
    'majorDirectHolders',
    'majorHoldersBreakdown',
    'price',
    'quoteType',
    'esgScores'
]


class YahooStockDetailsCollector(YahooApiSource, MetricCollector):
    MEASURE_NAME = "stock_details"
    MEASURE_NAME_2 = "recommendation_trend"

    async def measure_per_symbol(self) -> List[MetricEntry]:
        result: List[MetricEntry] = []
        for symbol in self.symbols:
            raw_res = await asyncio_detailed(client=self.client, symbol=symbol, modules=','.join(modules))
            res = json.loads(raw_res.content.decode())
            if 'quoteSummary' in res and 'result' in res['quoteSummary'] and len(res['quoteSummary']['result']) > 0:
                quote_summary_result = res['quoteSummary']['result'][0]
            else:
                raise ParseYahooResponseException('stock details response returned an unexpected response')

            if 'financialData' in quote_summary_result:
                result.append(MetricEntry(
                    measure_name=self.MEASURE_NAME,
                    symbol=symbol,
                    data=quote_summary_result['financialData']
                ))
            if 'recommendationTrend' in quote_summary_result \
                    and 'trend' in quote_summary_result['recommendationTrend'] \
                    and len(quote_summary_result['recommendationTrend']['trend']):
                result.append(MetricEntry(
                    measure_name=self.MEASURE_NAME_2,
                    symbol=symbol,
                    data=quote_summary_result['recommendationTrend']['trend'][0]
                ))
        return result
