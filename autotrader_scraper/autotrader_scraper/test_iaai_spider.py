import os
import sys
import logging

import django

from spiders.auction_spider_iaai_working import MergedAuctionSpider

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "./autotrader_scraper/"))
sys.path.append(os.path.join(os.path.abspath(os.getcwd()), "../../autotrader_web"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autotrader_web.autotrader.settings")
django.setup()

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


def scrape_auctions_task_copart(*args, **kwargs):
    crawl_pages = kwargs.get("crawl_pages", None)
    runner = CrawlerRunner()

    # Set up logging configuration
    logging.basicConfig(level=logging.DEBUG)  # Adjust the logging level as needed

    d = runner.crawl(MergedAuctionSpider, crawl_pages=1)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == "__main__":
    scrape_auctions_task_copart(crawl_pages=1)
