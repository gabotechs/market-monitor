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

from metric_publisher.influx_metric_publisher import InfluxMetricPublisher


class Config(PyArgs):
    symbols: List[str]
    influxdb_host: str = 'localhost'
    influxdb_port: int = 8086
    influxdb_token: str
    influxdb_bucket: str = 'primary'
    influxdb_organization: str = 'primary'
    log_level: str = 'INFO'
    twitter_token: Optional[str] = None


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
        logger.warning("TWITTER_TOKEN not configured, tweeter feed is not available")
    publisher.register_plugin(YahooIndexesCollector(), interval=5)
    publisher.register_plugin(YahooQuotesCollector(config.symbols), interval=5)
    publisher.register_plugin(YahooInsightsCollector(config.symbols), interval=3600)
    publisher.register_plugin(YahooStockDetailsCollector(config.symbols), interval=3600)
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
