from typing import List

from metric_publisher.metric_collector import MetricCollector, MetricEntry
from twitter_api import TwitterApi


class TwitterTweetCollector(MetricCollector):
    MEASURE_NAME = "twitter"

    def __init__(self, token: str):
        self.api = TwitterApi(token)

    async def get_metrics(self) -> List[MetricEntry]:
        new_tweets = self.api.get_tweets()
        metrics: List[MetricEntry] = []
        for new_tweet in new_tweets:
            metrics.append(MetricEntry(
                measure_name=self.MEASURE_NAME,
                data=new_tweet.__dict__,
                time=int(new_tweet.timestamp*1e9)
            ))
        return metrics
