from typing import Dict, List
import time
from pyargparse import PyArgs
import typing as T
from yahoo_finance_api import QuoteSource
import asyncio
import os
from influx_metric_publisher import InfluxMetricPublisher, MetricPublisherPlugin


class Config(PyArgs):
    interval: int = 5
    symbols: T.List[str]
    influxdb_host: str = 'localhost'
    influxdb_port: int = 8086
    influxdb_token: str = 'abcd'
    influxdb_bucket: str = 'primary'
    influxdb_organization: str = 'primary'


class QuotePlugin(MetricPublisherPlugin):
    async def measure_per_symbol(self, symbols: List[str]) -> Dict[str, dict]:
        data_per_symbol = await QuoteSource().retrieve(symbols)
        return {k: v.__dict__ for k, v in data_per_symbol.items()}


async def main():
    config = Config(os.environ.get("CONFIG_PATH") or 'config.yml')
    publisher = InfluxMetricPublisher(
        host=config.influxdb_host,
        port=config.influxdb_port,
        token=config.influxdb_token,
        bucket=config.influxdb_bucket,
        org=config.influxdb_organization,
        symbols=config.symbols
    )

    publisher.register_plugin(QuotePlugin("quote"))

    while True:
        start = time.time()
        await publisher.collect()
        print(f"collected metrics from {len(publisher.plugins)} plugins in {int((time.time() - start) * 1e3)} ms")
        for _ in range(config.interval):
            await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
