from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Optional


@dataclass
class MetricEntry:
    measure_name: str
    symbol: str
    data: dict
    time: Optional[int] = None


class MetricCollector(ABC):
    @abstractmethod
    async def measure_per_symbol(self) -> List[MetricEntry]:
        raise NotImplementedError()
