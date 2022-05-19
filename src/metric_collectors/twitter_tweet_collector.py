from typing import List
import time
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from metric_publisher.metric_collector import MetricCollector, MetricEntry
from twitter_api import TwitterApi


class TwitterTweetCollector(MetricCollector):
    MEASURE_NAME = "twitter"

    def __init__(self, token: str, logger: logging.Logger):
        self.analyzer = SentimentIntensityAnalyzer()
        self.logger = logger
        self.api = TwitterApi(token, logger)

    async def get_metrics(self) -> List[MetricEntry]:
        new_tweets = await self.api.get_tweets()
        metrics: List[MetricEntry] = []
        for new_tweet in new_tweets:
            time_ns = int(time.mktime(new_tweet.timestamp.timetuple())*1e9)
            sentiment = self.analyzer.polarity_scores(new_tweet.content)
            metrics.append(MetricEntry(
                measure_name=self.MEASURE_NAME,
                data={**new_tweet.__dict__, "sentiment": sentiment},
                time=time_ns
            ))
        return metrics
