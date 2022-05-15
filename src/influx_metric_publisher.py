from typing import List, Dict
from abc import ABC, abstractmethod
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import time
from influxdb_client import Point


class MetricPublisherPlugin(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def measure_per_symbol(self, symbols: List[str]) -> Dict[str, dict]:
        raise NotImplementedError()


class InfluxMetricPublisher:
    def __init__(self, host: str, port: int, token: str, bucket: str, org: str, symbols: List[str]):
        self.client = InfluxDBClientAsync(
            url=f'http://{host}:{port}',
            token=token
        )
        self.symbols = symbols
        self.bucket = bucket
        self.org = org
        self.plugins: List[MetricPublisherPlugin] = []

    def register_plugin(self, plugin: MetricPublisherPlugin):
        self.plugins.append(plugin)

    async def collect(self):
        now = int(time.time()*1e9)
        points: List[Point] = []
        for plugin in self.plugins:
            measure_per_symbol = await plugin.measure_per_symbol(self.symbols)
            for symbol, measure in measure_per_symbol.items():
                p = Point.measurement(plugin.name)
                p = p.tag("symbol", symbol)
                p = p.time(now)
                for k, v in measure.items():
                    p.field(k, v)
                points.append(p)

        write_api = self.client.write_api()
        for point in points:
            await write_api.write(bucket=self.bucket, org=self.org, record=point)
