from typing import List
from datetime import datetime
import time
from logging import Logger
from reddit_api import RedditApi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from metric_publisher.metric_collector import MetricCollector, MetricEntry

COMMUNITIES = [
    'stocks'
]


# https://github.com/influxdata/ui/issues/4609
def _process_text(text: str) -> str:
    return text.replace('\n', ' ')


class RedditPostCollector(MetricCollector):
    MEASURE_NAME = 'reddit'

    def __init__(self,
                 logger: Logger,
                 client_id: str,
                 client_secret: str,
                 password: str,
                 username: str):
        self.logger = logger
        self.analyzer = SentimentIntensityAnalyzer()
        self.reddit = RedditApi(client_id, client_secret, password, username)
        self.start_from = None

    async def get_metrics(self) -> List[MetricEntry]:
        new_posts = await self.reddit.get_posts(communities=COMMUNITIES, start=self.start_from)
        self.start_from = datetime.now()
        metrics: List[MetricEntry] = []
        for post in new_posts:
            sentiment = self.analyzer.polarity_scores(post.text)
            post_dict = {**post.__dict__, "text": _process_text(post.text)}
            metrics.append(MetricEntry(
                measure_name=self.MEASURE_NAME,
                time=int(time.mktime(post.timestamp.timetuple())*1e9),
                data={**post_dict, "sentiment": sentiment}
            ))
        return metrics
