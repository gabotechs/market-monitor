from typing import Dict, List
import time
from pyargparse import PyArgs
import typing as T
from yahoo_finance_api import QuoteSource
import asyncio
import os
import logging
from influx_metric_publisher import InfluxMetricPublisher, MetricPublisherPlugin
import logs


class Config(PyArgs):
    interval: int = 5
    symbols: T.List[str]
    influxdb_host: str = 'localhost'
    influxdb_port: int = 8086
    influxdb_token: str
    influxdb_bucket: str = 'primary'
    influxdb_organization: str = 'primary'


class QuotePlugin(MetricPublisherPlugin):
    async def measure_per_symbol(self, symbols: List[str]) -> Dict[str, dict]:
        data_per_symbol = await QuoteSource().retrieve(symbols)
        return {k: v.__dict__ for k, v in data_per_symbol.items()}


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
        symbols=config.symbols,
        logger=logger
    )

    publisher.register_plugin(QuotePlugin("quote"))
    logger.info(f"monitoring symbols {', '.join(config.symbols)}")
    try:
        await publisher.loop(config.interval)
    except Exception as e:
        logger.error('Error on main loop: '+str(e))
        exit(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
