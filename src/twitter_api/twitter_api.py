import tweepy
from typing import List
from dataclasses import dataclass
import time
import dateutil.parser

USER_IDS = [
    "@CNBC",
    "@Benzinga",
    "@Stocktwits",
    "@BreakoutStocks",
    "@bespokeinvest",
    "@WSJMarkets",
    "@Stephanie_Link",
    "@nytimesbusiness",
    "@IBDinvestors",
    "@WSJDealJournal"
]


@dataclass
class Tweet:
    user: str
    content: str
    timestamp: float


class TwitterApi:
    def __init__(self, token: str):
        self.api = tweepy.Client(bearer_token=token)
        self.user_ids = None
        self.last_requested = None

    def get_tweets(self) -> List[Tweet]:
        if self.user_ids is None:
            response = self.api.get_users(usernames=[x.replace("@", "") for x in USER_IDS])
            self.user_ids = {x.id: "@"+x.name for x in response.data}

        tweets: List[Tweet] = []
        last_requested = None
        for user_id in self.user_ids:
            response = self.api.get_users_tweets(
                id=user_id,
                start_time=self.last_requested,
                tweet_fields=["created_at"]
            )
            if response.data is None:
                continue
            for tweet in response.data:
                created_at = tweet.data.get("created_at")
                timestamp = dateutil.parser.isoparse(created_at)
                if last_requested is None or timestamp > last_requested:
                    last_requested = timestamp
                tweets.append(Tweet(
                    user=self.user_ids[user_id],
                    content=tweet.text,
                    timestamp=time.mktime(timestamp.timetuple())
                ))
        if last_requested:
            self.last_requested = last_requested
        return tweets


if __name__ == '__main__':
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAHipcQEAAAAAK7jM9ngfvlQOrq0PJ12cSmhIZbY%3DLX7KMWu3SXfMizN5ijXXg6vFK6jnaF5HKBSetVqy92iuPy5Jj6"
    api = TwitterApi(bearer_token)
    retrieved = api.get_tweets()
    re = api.get_tweets()
    print()
