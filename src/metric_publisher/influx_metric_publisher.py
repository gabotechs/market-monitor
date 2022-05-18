import asyncio
import time
import traceback
from dataclasses import dataclass
from logging import Logger
from typing import List

from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from .metric_collector import MetricCollector
from .utils.flatten_dict import flatten_dict


@dataclass
class PluginSpec:
    collector: MetricCollector
    interval_ns: int
    last_queried: int


class InfluxMetricPublisher:
    ERROR_MEASURE = "errors"

    def __init__(self, host: str, port: int, token: str, bucket: str, org: str, logger: Logger):
        self.client = InfluxDBClientAsync(
            url=f'http://{host}:{port}',
            token=token
        )
        self.bucket = bucket
        self.org = org
        self.plugins: List[PluginSpec] = []
        self.logger = logger

    async def wait_available(self):
        while True:
            try:
                await self.client.ping()
                break
            except Exception as e:
                self.logger.warning(f"Waiting for influx: ${e}")
                await asyncio.sleep(1)

    def register_plugin(self, collector: MetricCollector, interval: int):
        self.plugins.append(PluginSpec(
            collector=collector,
            interval_ns=int(interval * 1e9),
            last_queried=0
        ))

    async def __collect_points(self) -> List[Point]:
        now = int(time.time()*1e9)
        points: List[Point] = []

        tasks = []
        for plugin_spec in self.plugins:
            if now - plugin_spec.last_queried < plugin_spec.interval_ns:
                continue
            plugin_spec.last_queried = now

            async def task(plugin: PluginSpec):
                try:
                    metrics = await plugin.collector.get_metrics()
                except Exception as e:
                    self.logger.error(f"Error on plugin {plugin.collector.__class__.__name__}: {e}")
                    print(e)
                    traceback.print_exc()
                    return

                for metric in metrics:
                    p = Point.measurement(metric.measure_name)
                    if metric.tags:
                        for k, v in metric.tags.items():
                            p = p.tag(k, v)
                    if metric.time:
                        p = p.time(metric.time)
                    else:
                        p = p.time(now)
                    flatten_data = flatten_dict(metric.data)
                    for k, v in flatten_data.items():
                        p.field(k, v)
                    points.append(p)
            tasks.append(task(plugin_spec))

        await asyncio.gather(*tasks)
        return points

    async def loop(self):
        while True:
            start = time.time()
            points = await self.__collect_points()
            write_api = self.client.write_api()
            for point in points:
                try:
                    await write_api.write(bucket=self.bucket, org=self.org, record=point)
                except Exception as e:
                    self.logger.error(f"Error writing to influx: {e}")
            if len(points):
                self.logger.info(
                    f"collected {len(points)} metrics from "
                    f"{len(self.plugins)} plugins in {int((time.time() - start) * 1e3)} ms"
                )

            await asyncio.sleep(1)
