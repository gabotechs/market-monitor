import asyncio
import os
import traceback
from typing import List, Optional

from pyargparse import PyArgs

from collectable_logger import CollectableLogger
from metric_collectors.yahoo_quotes_collector import YahooQuotesCollector
from metric_collectors.yahoo_stock_details_collector import YahooStockDetailsCollector
from metric_collectors.yahoo_insights_collector import YahooInsightsCollector
from metric_collectors.yahoo_indexes_collector import YahooIndexesCollector
from metric_collectors.twitter_tweet_collector import TwitterTweetCollector
from metric_collectors.reddit_post_collector import RedditPostCollector

from metric_publisher.influx_metric_publisher import InfluxMetricPublisher


class Config(PyArgs):
    symbols: List[str]
    log_level: str = 'INFO'

    influxdb_host: str = 'localhost'
    influxdb_port: int = 8086
    influxdb_token: str
    influxdb_bucket: str = 'primary'
    influxdb_organization: str = 'primary'

    twitter_token: Optional[str] = None

    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_password: Optional[str] = None
    reddit_username: Optional[str] = None


async def main():
    config = Config(os.environ.get("CONFIG_PATH") or 'config.yml')
    logger = CollectableLogger("main", config.log_level)
    logger.info("Initializing metric publisher...")
    publisher = InfluxMetricPublisher(
        host=config.influxdb_host,
        port=config.influxdb_port,
        token=config.influxdb_token,
        bucket=config.influxdb_bucket,
        org=config.influxdb_organization,
        logger=logger
    )

    await publisher.wait_available()

    if config.twitter_token:
        publisher.register_plugin(TwitterTweetCollector(config.twitter_token, logger), interval=600)
    else:
        logger.warning("TWITTER_TOKEN not configured, twitter feed is not available")

    if config.reddit_username and config.reddit_password and config.reddit_client_id and config.reddit_client_secret:
        publisher.register_plugin(RedditPostCollector(logger, config.reddit_client_id, config.reddit_client_secret, config.reddit_password, config.reddit_username), interval=3600)
    else:
        logger.warning("REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_PASSWORD or REDDIT_USERNAME not configured, reddit feed is not available")

    publisher.register_plugin(YahooIndexesCollector(logger), interval=5)
    publisher.register_plugin(YahooQuotesCollector(config.symbols, logger), interval=5)
    publisher.register_plugin(YahooInsightsCollector(config.symbols, logger), interval=3600)
    publisher.register_plugin(YahooStockDetailsCollector(config.symbols, logger), interval=3600)
    publisher.register_plugin(logger, interval=5)

    logger.info(f"monitoring symbols {', '.join(config.symbols)}")
    try:
        await publisher.loop()
    except Exception as e:
        logger.error('Error on main loop: '+str(e))
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
