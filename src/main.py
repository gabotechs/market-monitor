import asyncio
import os
import traceback
from typing import List

from pyargparse import PyArgs

import logs
from metric_collectors.yahoo_quotes_collector import YahooQuotesCollector
from metric_collectors.yahoo_stock_details_collector import YahooStockDetailsCollector
from metric_collectors.yahoo_insights_collector import YahooInsightsCollector
from metric_collectors.yahoo_indexes_collector import YahooIndexesCollector

from metric_publisher.influx_metric_publisher import InfluxMetricPublisher


class Config(PyArgs):
    symbols: List[str]
    influxdb_host: str = 'localhost'
    influxdb_port: int = 8086
    influxdb_token: str
    influxdb_bucket: str = 'primary'
    influxdb_organization: str = 'primary'


async def main():
    config = Config(os.environ.get("CONFIG_PATH") or 'config.yml')
    logger = logs.init_logger()
    logger.info("Initializing metric publisher...")
    publisher = InfluxMetricPublisher(
        host=config.influxdb_host,
        port=config.influxdb_port,
        token=config.influxdb_token,
        bucket=config.influxdb_bucket,
        org=config.influxdb_organization,
        logger=logger
    )

    await publisher.wait_available()

    publisher.register_plugin(YahooIndexesCollector(), interval=5)
    publisher.register_plugin(YahooQuotesCollector(config.symbols), interval=5)
    publisher.register_plugin(YahooInsightsCollector(config.symbols), interval=3600)
    publisher.register_plugin(YahooStockDetailsCollector(config.symbols), interval=3600)

    logger.info(f"monitoring symbols {', '.join(config.symbols)}")
    try:
        await publisher.loop()
    except Exception as e:
        logger.error('Error on main loop: '+str(e))
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
