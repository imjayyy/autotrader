import datetime
import json
import logging
import math
import random

import scrapy
from django.utils import timezone
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.retry import get_retry_request

from items import Auction
from pipelines import SaveData

try:
    from autotrader_scraper.autotrader_scraper.middlewares import  PROXY_IPs
except ImportError:
    from middlewares import PROXY_IPs

logger = logging.getLogger(__name__)


class AuctionSpiderCopartEfficient(scrapy.Spider):
    name = 'auction_spider_copart'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ua = UserAgent()
        self.lots_per_search = 20
        self.start_urls = ["https://www.copart.com/public/lots/search-results"]

    custom_settings = {
        # 'ROTATING_PROXY_LIST': random.choice(PROXY_IPs)s,
        # 'ROTATING_PROXY_PAGE_RETRY_TIMES': 50,
        'RETRY_TIMES': 10,
        'DOWNLOADER_MIDDLEWARES': {
            # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 950,
            # 'rotating_proxies.middlewares.BanDetectionMiddleware': 960,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,

        },
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def start_requests(self):
        # Send a request to start scraping
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                method='POST',
                headers={
                    'Authority': 'www.copart.com',
                    'Content-Type': 'application/json',
                    'User-Agent': self.ua.random,
                    'Host': 'www.copart.com'

                },
                body='{"query":["*"],"filter":{},"sort":["auction_date_type desc",'
                     '"auction_date_utc asc"],"size":'
                     + str(self.lots_per_search)
                     + ',"watchListOnly":false,'
                       '"freeFormSearch":false, '
                       '"hideImages":false,"defaultSort":false,'
                       '"specificRowProvided":false,"displayName":"",'
                       '"searchName":"","backUrl":"","includeTagByField":{'
                       '},"rawParams":{}}',
                meta={"proxy": random.choice(PROXY_IPs),
                      'page': 0}  # Initial page number
            )

    def parse(self, response):
        # Parse the search results page
        if response.status == 200:
            url = "https://www.copart.com/public/lots/search-results"
            try:
                total_pages = int(self.crawl_pages)
            except:
                try:
                    res = json.loads(response.text)
                    total_pages = res["data"]["results"]["totalElements"]
                    total_pages = math.ceil(int(total_pages) / self.lots_per_search)
                except Exception as e:
                    total_pages = 1

            for page in range(total_pages):
                request_data = {
                    "query": ["*"],
                    "filter": {},
                    "sort": ["auction_date_type desc", "auction_date_utc asc"],
                    "page": page,
                    "size": self.lots_per_search,
                    "start": (page - 1) * self.lots_per_search,
                    "watchListOnly": False,
                    "freeFormSearch": False,
                    "hideImages": False,
                    "defaultSort": False,
                    "specificRowProvided": False,
                    "displayName": "",
                    "searchName": "",
                    "backUrl": "",
                    "includeTagByField": {},
                    "rawParams": {},
                }

                yield scrapy.Request(
                    url,
                    method='POST',
                    headers={
                        'Authority': 'www.copart.com',
                        'Content-Type': 'application/json',
                        'User-Agent': self.ua.random,
                        'Host': 'www.copart.com'

                    },
                    body=json.dumps(request_data),
                    callback=self.parse_page,
                    meta={"proxy": random.choice(PROXY_IPs),
                          'page': page, 'lots_per_search': self.lots_per_search}
                )

        else:
            print(response.text)

    def parse_page(self, response):
        # Parse each page of search results
        try:
            if response.status == 200:
                response_json = json.loads(response.text)
                page = response.meta['page']
                lots_per_search = response.meta['lots_per_search']
                contents = response_json["data"]["results"]["content"]
                for index, value in enumerate(contents):
                    # Process each auction item
                    id = value['ln']
                    yield scrapy.Request(
                        f"https://www.copart.com/public/data/lotdetails/solr/lotImages/{id}/USA",
                        headers={
                            'Authority': 'www.copart.com',
                            'Content-Type': 'application/json',
                            'User-Agent': self.ua.random,
                            'Host': 'www.copart.com'

                        },
                        callback=self.parse_item,
                        meta={"proxy": random.choice(PROXY_IPs),
                              'page': page, 'lots_per_search': lots_per_search, 'content': value}
                    )

        except Exception as e:
            # Retry the request if it fails
            new_request_or_none = get_retry_request(
                response.request,
                spider=self,
                reason='Unable to parse page data',
            )
            return new_request_or_none

    def parse_item(self, response):
        # Parse the details of each auction item
        try:
            if response.status == 200:
                response_json = json.loads(response.text)
                each = response.meta['content']

                if "ad" in each.keys():
                    item = Auction()
                    item["SearchTerm"] = ""
                    keys = {
                        "Year": "lcy",
                        "Make": "mkn",
                        "ModelGroup": "lmg",
                        "Model": "lm",
                        "PrimaryDamage": "dd",
                        "SecondaryDamage": "sdd",
                        "Vin": "fv",
                        "LocationName": "yn",
                        "ImageFull": "tims",
                        "ImageThumb": "tims",
                        "SaleDate": "ad",
                        "EngineSize": "egn",
                        "OdometerType": "ord",
                        "LotId": "ln",
                        "Odometer": "orr",
                    }

                    for key in keys.keys():
                        if keys[key] in each.keys():
                            item[key] = each[keys[key]]
                        else:
                            item[key] = None

                    item["DateCreated"] = datetime.datetime.now(timezone.utc)
                    item["BodyStyle"] = None
                    item["SearchTerm"] = ""
                    item["SaleDate"] = datetime.datetime.fromtimestamp(
                        ((int)(each["ad"])) / 1000
                    )
                    item["Currency"] = "USD"
                    item["SaleStatus"] = each["dynamicLotDetails"]["saleStatus"]
                    item["BidStatus"] = each["dynamicLotDetails"]["bidStatus"]
                    item["CurrentBid"] = each["dynamicLotDetails"]["currentBid"]
                    item["VinHash"] = None
                    item["LastUpdated"] = datetime.datetime.now(tz=timezone.utc)

                    if item["LocationName"] is not None:
                        item["LocationName"] = item["LocationName"][5:]

                    if "lu" in each.keys():
                        item["LastUpdated"] = datetime.datetime.fromtimestamp(
                            ((int)(each["lu"])) / 1000
                        )

                    item["Lane"] = each["al"] if "al" in each.keys() else None
                    item["Item"] = each["aan"] if "aan" in each.keys() else None
                    item["Grid"] = each["gr"] if "gr" in each.keys() else None
                    item["AuctionCompanyId"] = 1

                    item["Color"] = None
                    item["Transmission"] = None
                    item["Drive"] = None
                    item["VehicleType"] = None
                    item["Cylinders"] = None
                    item["Fuel"] = None
                    item["Keys"] = None

                    if item["Make"] is not None and item["Model"] is not None:
                        item["SearchTerm"] = item["Make"] + item["Model"]

                    if "data" in response_json.keys():
                        if "imagesList" in response_json["data"].keys():
                            item["Images"] = response_json["data"]["imagesList"]

                        if "lotDetails" in response_json["data"].keys():
                            response_json["data"]["lotDetails"] = self.model_response_additional_info(
                                response_json["data"]["lotDetails"]
                            )
                            item["Color"] = response_json["data"]["lotDetails"]["clr"]
                            item["VehicleType"] = response_json["data"]["lotDetails"]["vehTypDesc"]
                            item["Transmission"] = response_json["data"]["lotDetails"]["tsmn"]
                            item["Cylinders"] = response_json["data"]["lotDetails"]["cy"]
                            item["Fuel"] = response_json["data"]["lotDetails"]["ft"]
                            item["Keys"] = response_json["data"]["lotDetails"]["hk"]
                            item["Drive"] = response_json["data"]["lotDetails"]["drv"]

                    save_data_pipeline = SaveData()
                    save_data_pipeline.process_item(item)
        except Exception as e:
            # Retry the request if it fails
            new_request_or_none = get_retry_request(
                response.request,
                spider=self,
                reason='Unable to parse item data',
            )
            return new_request_or_none

    def model_response_additional_info(self, response):
        # Helper method to fill missing keys with None
        keys = [
            "gr",
            "al",
            "aan",
            "orr",
            "clr",
            "vehTypDesc",
            "ad",
            "tsmn",
            "cy",
            "ft",
            "hk",
            "drv",
        ]
        for key in keys:
            if key not in response.keys():
                response[key] = None
        return response
