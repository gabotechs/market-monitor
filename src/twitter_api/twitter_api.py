from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import dateutil.parser
import httpx
import platform
import logging

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
    # "@WSJDealJournal"
]

HOST = "https://api.twitter.com"


@dataclass
class Tweet:
    user: str
    content: str
    timestamp: datetime


# https://github.com/influxdata/ui/issues/4609
def _process_text(text: str) -> str:
    return text.replace('\n', ' ')


class TwitterApi:
    def __init__(self, token: str, logger: logging.Logger):
        self.logger = logger
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': platform.python_version(),
                'Authorization': 'Bearer ' + token
            }
        )
        self.token = token
        self.user_ids: Optional[Dict[str, str]] = None
        self.last_requested = None

    async def __load_user_ids(self) -> Dict[str, str]:
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
            user_ids[user['id']] = "@" + user['name']
        self.user_ids = user_ids
        return user_ids

    async def __get_user_tweets(self, user_id: str, start_time: Optional[datetime]) -> List[Tweet]:
        params = {'tweet.fields': 'created_at'}
        if start_time:
            params['start_time'] = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        response = await self.client.get(
            url=HOST + f"/2/users/{user_id}/tweets",
            params=params
        )
        if response.status_code != 200:
            raise Exception(f'Received a {response.status_code} code from twitter')
        data = response.json()
        if 'data' not in data:
            raise Exception('Badly formed twitter response')
        tweets = []
        for tweet in data['data']:
            if 'created_at' not in tweet or 'text' not in tweet:
                raise Exception('Badly formed twitter response')
            tweets.append(Tweet(
                user=self.user_ids[user_id],
                content=_process_text(tweet['text']),
                timestamp=dateutil.parser.isoparse(tweet['created_at'])
            ))
        return tweets

    async def get_tweets(self) -> List[Tweet]:
        if self.user_ids is None:
            self.logger.info("loading user ids...")
            loaded_user_ids = await self.__load_user_ids()
            self.logger.info(f"{len(loaded_user_ids)} users loaded correctly")

        tweets: List[Tweet] = []
        last_requested = None
        self.logger.info(f"collecting tweets since {self.last_requested}...")
        for user_id in self.user_ids:
            user_tweets = await self.__get_user_tweets(user_id, self.last_requested)
            for tweet in user_tweets:
                if last_requested is None or tweet.timestamp > last_requested:
                    last_requested = tweet.timestamp
            tweets = [*tweets, *user_tweets]
        self.logger.info(f"collected {len(tweets)} new tweets")
        if last_requested:
            self.last_requested = last_requested
        return tweets
