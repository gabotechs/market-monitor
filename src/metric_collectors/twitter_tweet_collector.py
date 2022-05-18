from typing import List
import time

from metric_publisher.metric_collector import MetricCollector, MetricEntry
from twitter_api import TwitterApi


class TwitterTweetCollector(MetricCollector):
    MEASURE_NAME = "twitter"

    def __init__(self, token: str):
        self.api = TwitterApi(token)

    async def get_metrics(self) -> List[MetricEntry]:
        new_tweets = await self.api.get_tweets()
        metrics: List[MetricEntry] = []
        for new_tweet in new_tweets:
            time_ns = int(time.mktime(new_tweet.timestamp.timetuple())*1e9)
            metrics.append(MetricEntry(
                measure_name=self.MEASURE_NAME,
                data=new_tweet.__dict__,
                time=time_ns
            ))
        return metrics
