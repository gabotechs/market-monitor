import tweepy
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import time
import dateutil.parser
import httpx
import platform

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

HOST = "https://api.twitter.com"


@dataclass
class Tweet:
    user: str
    content: str
    timestamp: datetime


class TwitterApi:
    def __init__(self, token: str):
        self.api = tweepy.Client(bearer_token=token)
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': platform.python_version(),
                'Authorization': 'Bearer '+token
            }
        )
        self.token = token
        self.user_ids = None
        self.last_requested = None

    async def __load_user_ids(self):
        response = await self.client.get(
            url=HOST + "/2/users/by",
            params={'usernames': ','.join([x.replace("@", "") for x in USER_IDS])}
        )
        data = response.json()
        if 'data' not in data or type(data['data']) != list:
            raise Exception('Badly formed twitter response')
        user_ids = {}
        for user in data['data']:
            if 'id' not in user or 'name' not in user:
                raise Exception('Badly formed twitter response')
            user_ids[user['id']] = "@"+user['name']
        self.user_ids = user_ids

    async def __get_user_tweets(self, user_id: str, start_time: Optional[datetime]) -> List[Tweet]:
        params = {'tweet.fields': 'created_at'}
        if start_time:
            params['start_time'] = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        response = await self.client.get(
            url=HOST+f"/2/users/{user_id}/tweets",
            params=params
        )
        data = response.json()
        if 'data' not in data:
            raise Exception('Badly formed twitter response')
        tweets = []
        for tweet in data['data']:
            if 'created_at' not in tweet or 'text' not in tweet:
                raise Exception('Badly formed twitter response')
            tweets.append(Tweet(
                user=self.user_ids[user_id],
                content=tweet['text'],
                timestamp=dateutil.parser.isoparse(tweet['created_at'])
            ))
        return tweets

    async def get_tweets(self) -> List[Tweet]:
        if self.user_ids is None:
            await self.__load_user_ids()

        tweets: List[Tweet] = []
        last_requested = None
        for user_id in self.user_ids:
            user_tweets = await self.__get_user_tweets(user_id, self.last_requested)
            tweets = [*tweets, *user_tweets]
        if last_requested:
            self.last_requested = last_requested
        return tweets


if __name__ == '__main__':
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAHipcQEAAAAAK7jM9ngfvlQOrq0PJ12cSmhIZbY%3DLX7KMWu3SXfMizN5ijXXg6vFK6jnaF5HKBSetVqy92iuPy5Jj6"
    api = TwitterApi(bearer_token)
    retrieved = api.get_tweets()
    re = api.get_tweets()
    print()
