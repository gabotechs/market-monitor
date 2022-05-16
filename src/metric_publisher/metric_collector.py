from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


@dataclass
class MetricEntry:
    measure_name: str
    data: dict
    tags: Optional[Dict[str, str]] = None
    time: Optional[int] = None


class MetricCollector(ABC):
    @abstractmethod
    async def get_metrics(self) -> List[MetricEntry]:
        raise NotImplementedError()
