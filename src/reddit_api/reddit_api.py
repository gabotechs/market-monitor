from dataclasses import dataclass
from datetime import datetime
from typing import List
import asyncpraw
import asyncpraw.models


@dataclass
class RedditPost:
    community: str
    timestamp: datetime
    text: str
    link: str


class RedditApi:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 password: str,
                 username: str
                 ):
        self.client = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            password=password,
            user_agent=f'Post collector app by u/{username}',
            username=username,
        )

    async def get_posts(self, communities: List[str], start: datetime = None) -> List[RedditPost]:
        generators = await self.client.subreddit('+'.join(communities))
        posts = []
        async for submission in generators.new():
            if not isinstance(submission, asyncpraw.models.Submission):
                continue
            post = RedditPost(
                community=submission.subreddit_name_prefixed,
                timestamp=datetime.fromtimestamp(submission.created_utc),
                text=submission.selftext,
                link=submission.url
            )
            if start is not None and post.timestamp < start:
                break
            posts.append(post)

        return posts
