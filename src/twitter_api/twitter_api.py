import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import dateutil.parser
import httpx
import platform
import logging
import json

USER_IDS = {
    "@CNBC",
    "@Benzinga",
    "@Stocktwits",
    "@WSJMarkets",
    "@bespokeinvest",
    "@BreakoutStocks",
    "@Stephanie_Link",
    "@nytimesbusiness",
    "@IBDinvestors",
    "@WSJDealJournal",
    "@elonmusk",
    "@Newsweek",
    "@WashingtonPost",
    "@jimcramer",
    "@TheStalwart",
    "@TruthGundlach",
    "@Carl_C_Icahn",
    "@ReformedBroker",
    "@bespokeinvest",
    "@stlouisfed",
    "@muddywatersre",
    "@mcuban",
    "@AswathDamodaran",
    "@elerianm",
    "@MorganStanley",
    "@ianbremmer",
    "@GoldmanSachs",
    "@Wu_Tang_Finance",
    "@Schuldensuehner",
    "@NorthmanTrader",
    "@Frances_Coppola",
    "@bySamRo",
    "@BuzzFeed",
    "@nytimes"
}

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
        self.last_requested: Optional[datetime] = None

    async def __load_user_ids(self) -> Dict[str, str]:
        response = await self.client.get(
            url=HOST + "/2/users/by",
            params={'usernames': ','.join([x.replace("@", "") for x in USER_IDS])}
        )
        if response.status_code != 200:
            raise Exception(f'Received a {response.status_code} while getting user ids from twitter')
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
            raise Exception(f'Received a {response.status_code} code while getting tweets for {user_id} from twitter')
        data = response.json()
        if 'data' not in data:
            return []
        tweets = []
        for tweet in data['data']:
            if 'created_at' not in tweet or 'text' not in tweet:
                raise Exception(f'Badly formed twitter response {json.dumps(tweet)}')
            tweets.append(Tweet(
                user=self.user_ids[user_id],
                content=_process_text(tweet['text']),
                timestamp=dateutil.parser.isoparse(tweet['created_at'])
            ))
        return tweets

    @dataclass
    class TaskContext:
        fail_count: int
        last_requested: Optional[datetime]
        tweets: List[Tweet]

    async def task(self, user_id: str, context: TaskContext):
        if context.fail_count > len(self.user_ids) / 3:
            return
        try:
            user_tweets = await self.__get_user_tweets(user_id, self.last_requested)
        except Exception as e:
            self.logger.error(f'Failed to get tweets: {e}')
            context.fail_count += 1
            if context.fail_count > len(self.user_ids) / 3:
                raise Exception(f'Too much failures getting tweets')
            return
        for tweet in user_tweets:
            if context.last_requested is None or tweet.timestamp > context.last_requested:
                context.last_requested = tweet.timestamp
        context.tweets.extend(user_tweets)
        try:
            print(self.user_ids[user_id], user_tweets[-1].timestamp)
        except:
            print(self.user_ids[user_id], None)

    async def get_tweets(self) -> List[Tweet]:
        if self.user_ids is None:
            self.logger.info("loading user ids...")
            loaded_user_ids = await self.__load_user_ids()
            self.logger.info(f"{len(loaded_user_ids)} users loaded correctly")

        self.logger.info(f"collecting tweets since {self.last_requested}...")

        tasks_context = self.TaskContext(
            fail_count=0,
            last_requested=None,
            tweets=[]
        )

        tasks = []
        for user_id in self.user_ids:
            tasks.append(self.task(user_id, tasks_context))
        await asyncio.gather(*tasks)
        self.logger.info(f"collected {len(tasks_context.tweets)} new tweets")
        if tasks_context.last_requested:
            self.last_requested = tasks_context.last_requested
        return tasks_context.tweets
