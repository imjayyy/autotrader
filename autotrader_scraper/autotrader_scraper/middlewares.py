import random

from scrapy import signals

from itemadapter import is_item, ItemAdapter

# PROXY_IP = "http://37.48.118.90:13042"
PROXY_IPs = ["http://37.48.118.90:13042", "http://83.149.70.159:13042"]
# PROXY_IPs = [
#     "http://brd-customer-hl_a14c1bed-zone-zone3:8ovmla1xk3po@zproxy.lum-superproxy.io:22225"]
#              # "http://brd-customer-hl_a14c1bed-zone-zone3:8ovmla1xk3po@zproxy.lum-superproxy.io:22225"]
# PROXY_IP = "http://brd-customer-hl_a14c1bed-zone-zone3:8ovmla1xk3po@zproxy.lum-superproxy.io:22225"

PROXY_IP = random.choice(PROXY_IPs)


class AutotraderScraperSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AutotraderScraperDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ProxiesDownloaderMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = PROXY_IP
