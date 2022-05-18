import logging
from dataclasses import dataclass
from collections import deque
from typing import List, Deque
import time

import coloredlogs
from metric_publisher.metric_collector import MetricCollector, MetricEntry


@dataclass
class LogEntry:
    msg: str
    level: str


class CollectableLogger(logging.Logger, MetricCollector):
    MEASURE_NAME = "logs"

    async def get_metrics(self) -> List[MetricEntry]:
        metrics = []
        for stored in self.store:
            metrics.append(MetricEntry(
                measure_name=self.MEASURE_NAME,
                data=stored.__dict__,
                time=int(time.time()*1e9)
            ))
        self.store.clear()
        return metrics

    def __init__(self, name: str, level: str):
        super(CollectableLogger, self).__init__(name, logging.__dict__[level.upper()])
        coloredlogs.install(logger=self)
        self.propagate = False
        self.store: Deque[LogEntry] = deque(maxlen=10000)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self.store.append(LogEntry(msg, "debug"))
        super().debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.store.append(LogEntry(msg, "info"))
        super().info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.store.append(LogEntry(msg, "warning"))
        super().warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.store.append(LogEntry(msg, "error"))
        super().error(msg, *args, **kwargs)

