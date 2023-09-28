import datetime
import json
# print("=" * 100)
# # Print Current Working Directory
# print("Current Working Directory " + os.getcwd())
# print("=" * 100)
import logging
import re

import scrapy
from django.utils import timezone

# sys.path.append("./autotrader_scraper/autotrader_scraper/")
# sys.path.append("./autotrader_web/")

try:
    from autotrader_scraper.autotrader_scraper.middlewares import PROXY_IP, PROXY_IPs
except ImportError:
    from middlewares import PROXY_IP, PROXY_IPs
logger = logging.getLogger(__name__)


class Auction(scrapy.Item):
    LotId = scrapy.Field()
    Year = scrapy.Field()
    Make = scrapy.Field()
    ModelGroup = scrapy.Field()
    Model = scrapy.Field()
    BodyStyle = scrapy.Field()
    Color = scrapy.Field()
    PrimaryDamage = scrapy.Field()
    Vin = scrapy.Field()
    Odometer = scrapy.Field()
    EngineSize = scrapy.Field()
    LocationName = scrapy.Field()
    VehicleType = scrapy.Field()
    ImageFull = scrapy.Field()
    ImageThumb = scrapy.Field()
    VinHash = scrapy.Field()
    SaleDate = scrapy.Field()
    SearchTerm = scrapy.Field()
    DateCreated = scrapy.Field()
    OdometerType = scrapy.Field()
    Currency = scrapy.Field()
    Images = scrapy.Field()
    Grid = scrapy.Field()
    Row = scrapy.Field()
    Lane = scrapy.Field()
    Item = scrapy.Field()
    LastUpdated = scrapy.Field()
    SaleStatus = scrapy.Field()
    BidStatus = scrapy.Field()
    CurrentBid = scrapy.Field()
    Transmission = scrapy.Field()
    Drive = scrapy.Field()
    Cylinders = scrapy.Field()
    Fuel = scrapy.Field()
    Keys = scrapy.Field()
    SecondaryDamage = scrapy.Field()
    AuctionCompanyId = scrapy.Field()
    BuyItNow = scrapy.Field()


class MergedAuctionSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(MergedAuctionSpider, self).__init__(*args, **kwargs)
        self.lots_per_search = "100"
        self.start_urls = [
            "https://www.iaai.com/Search?c=1686811670177",
        ]

    name = "merged_auction_spider"

    custom_settings = {
        'ITEM_PIPELINES': {
            'pipelines.SaveData': 400
        },
        'ROTATING_PROXY_LIST': PROXY_IPs,
        'ROTATING_PROXY_PAGE_RETRY_TIMES': 1,
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 950,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 960,
        }

    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.http.Request(
                url=url,
                method="POST",
                callback=self.start_scraper_loop,
                headers={
                    "content-type": "application/json",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/94.0.4606.81 Chrome/94.0.4606.81 Safari/537.36",
                },
                body='{"Searches":[{"Facets":[{"Group":"Availability","Value":"Items With a Sale Date"}],"FullSearch":null,"LongRanges":null},{"Facets":null,"FullSearch":null,"LongRanges":[{"From":2013,"Name":"Year","To":2024}]}],"ZipCode":"","miles":0,"PageSize":100,"CurrentPage":1,"Sort":[{"IsGeoSort":false,"SortField":"AuctionDateTime","IsDescending":false}],"SaleStatusFilters":[{"SaleStatus":0,"IsSelected":true}],"BidStatusFilters":[{"BidStatus":6,"IsSelected":true}]}',
            )

    def start_scraper_loop(self, response):
        url = self.start_urls[0]

        try:
            total_vehicles = (
                response.css("#TotalVehicleAmount")
                .css("::text")
                .extract()[0]
                .replace(" ", "")
            )
            total_vehicles = int(total_vehicles)
            total_pages = int(total_vehicles / int(self.lots_per_search))
        except:
            total_pages = 1

        total_pages = 10

        total_pages = self.crawl_pages if hasattr(self, "crawl_pages") else total_pages

        for page in range(int(total_pages)):
            yield scrapy.http.Request(
                url=url,
                method="POST",
                callback=self.parse_list,
                headers={
                    "content-type": "application/json",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/94.0.4606.81 Chrome/94.0.4606.81 Safari/537.36",
                },
                body='{"Searches":[{"Facets":[{"Group":"InventoryTypes","Value":"Automobiles"}],"FullSearch":null,"LongRanges":null},{"Facets":[{"Group":"IsDemo","Value":"False"}],"FullSearch":null,"LongRanges":null},{"Facets":[{"Group":"Market","Value":"United States"}],"FullSearch":null,"LongRanges":null},{"Facets":null,"FullSearch":null,"LongRanges":[{"From":2006,"Name":"Year","To":2023}]},{"Facets":[{"Group":"Availability","Value":"Items With a Sale Date"}],"FullSearch":null,"LongRanges":null}],"ZipCode":"","miles":0,"PageSize":'
                     + str(self.lots_per_search)
                     + ',"CurrentPage":'
                     + str(page)
                     + ',"Sort":[{"IsGeoSort":false,"SortField":"AuctionDateTime","IsDescending":false}],"SaleStatusFilters":[{"SaleStatus":0,"IsSelected":true}],"BidStatusFilters":[{"BidStatus":6,"IsSelected":true}]}',
            )

    def parse_list(self, response):
        urls = response.css("div.table-row.table-row-border")

        for url in urls:
            try:
                url = url.css("h4 a::attr(href)").extract()[0]
                url = f"https://www.iaai.com{url}"
                print(url)
                yield scrapy.Request(
                    url=url,
                    headers={
                        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/94.0.4606.81 Chrome/94.0.4606.81 Safari/537.36",
                    },
                    callback=self.parse_auction,
                    meta={"auction_id": url.split("/")[-1]},
                )
            except:
                pass
        # for item in response.xpath('//li[@class="search-results-listing"]'):
        #     auction_url = item.xpath('.//a[@class="link-unstyled"]/@href').extract_first()
        #     auction_id = re.search(r'VehicleID=(\d+)', auction_url).group(1)
        #     url = 'https://www.iaai.com/VehicleDetails?itemid=' + auction_id
        #     print(url)
        #     yield scrapy.Request(url='https://www.iaai.com' + auction_url, callback=self.parse_auction, meta={'auction_id': auction_id})

    def parse_auction(self, response):
        item = Auction()
        item["Images"] = {"FULL_IMAGE": []}

        try:
            lotdetails_script_json = response.css("#ProductDetailsVM::text").extract()[
                0
            ]
            lotdetails_script_json = json.loads(lotdetails_script_json)
            lotdetails_script_json = lotdetails_script_json["inventoryView"][
                "imageDimensions"
            ]["keys"]["$values"]
            for x in lotdetails_script_json:
                item["Images"]["FULL_IMAGE"].append(
                    {
                        "url": "https://vis.iaai.com/resizer?imageKeys="
                               + x["k"]
                               + "&width=845&height=633"
                    }
                )
        except:
            pass

        item["LotId"] = (
            response.url.split("VehicleDetail/")[1].replace("~", "").replace("US", "")
        )
        item["Model"] = self.get_prop(response, "Model:")
        item["BodyStyle"] = self.get_prop(response, "Body Style:")
        item["Vin"] = self.get_prop(response, "VIN (Status):")
        item["PrimaryDamage"] = self.get_prop(response, "Primary Damage:")
        item["LocationName"] = self.get_prop(response, "Selling Branch:")
        item["Odometer"] = (
            self.get_prop(response, "Odometer:")
            .split("(")[0]
            .replace("mi", "")
            .replace(",", "")
        )
        item["OdometerType"] = (
            self.get_prop(response, "Odometer:")
            .split("(")[1]
            .replace(")", "")
            .replace(",", "")
        )
        item["EngineSize"] = self.get_prop(response, "Engine:")
        item["VehicleType"] = self.get_prop(response, "Vehicle:")
        item["ModelGroup"] = self.get_prop(response, "Series:")
        item["Color"] = self.get_prop(response, "Exterior/Interior:").split("/")[0]
        try:
            item["Year"] = (
                response.css(
                    "body > section > main > section.section.section--vehicle-title > div:nth-child(2) > div > div > h1"
                )
                .css("::text")
                .extract()[0]
                .split(" ")[0]
            )
        except:
            item["Year"] = ""

        try:
            item["Make"] = (
                response.css(
                    "body > section > main > section.section.section--vehicle-title > div:nth-child(2) > div > div > h1"
                )
                .css("::text")
                .extract()[0]
                .split(" ")[1]
            )
        except:
            item["Make"] = ""
        item["SearchTerm"] = (
                item["Model"] + " " + item["Make"] + " " + item["BodyStyle"]
        )
        item["DateCreated"] = datetime.datetime.now(tz=timezone.utc)
        item["LastUpdated"] = datetime.datetime.now(tz=timezone.utc)
        item["SaleDate"] = self.get_prop(response, "Auction Date and Time:")
        item["Fuel"] = self.get_prop(response, "Fuel Type:")
        item["Transmission"] = self.get_prop(response, "Transmission:")
        item["Drive"] = self.get_prop(response, "Drive Line Type:")
        item["Cylinders"] = self.get_prop(response, "Cylinders:").replace(
            "Cylinders", ""
        )
        item["SecondaryDamage"] = None
        item["BidStatus"] = None
        item["SaleStatus"] = None
        item["VinHash"] = ""
        item["AuctionCompanyId"] = 2
        item["LocationName"] = (
            item["LocationName"][0:-4] if item["LocationName"] is not None else None
        )
        item["EngineSize"] = (
            None if "UNKNOWN" in item["EngineSize"] else item["EngineSize"]
        )
        item["Keys"] = "YES" if "Present" in self.get_prop(response, "Key:") else None

        try:
            item["Row"] = self.get_prop(response, "Aisle/Stall:").split("-")[1]
        except:
            item["Row"] = None

        try:
            item["Grid"] = self.get_prop(response, "Aisle/Stall:").split("-")[0]
        except:
            item["Grid"] = None

        try:
            item["Item"] = self.get_prop(response, "Lane/Run #:").split("-")[1]
        except:
            item["Item"] = None

        try:
            item["Lane"] = self.get_prop(response, "Lane/Run #:").split("-")[0]
        except:
            item["Lane"] = None

        try:
            item["ImageFull"] = item["Images"]["FULL_IMAGE"][0]["url"]
            item["ImageThumb"] = item["Images"]["FULL_IMAGE"][0]["url"]
        except:
            item["ImageFull"] = None
            item["ImageThumb"] = None

        try:
            item["CurrentBid"] = self.get_prop(response, "Current Bid:").group("price")
            item["Currency"] = self.get_currency(
                self.get_prop(response, "Current Bid:").group("currency")
            )
        except:
            item["CurrentBid"] = None
            item["Currency"] = None

        try:
            if (
                    len(
                        response.css(".btn.btn-md.btn-primary.btn-block.btn--buy-now")[0]
                                .css("::text")
                                .extract()
                    )
                    > 0
            ):
                item["BuyItNow"] = 1
            else:
                item["BuyItNow"] = 0
        except:
            item["BuyItNow"] = 0

        # print("=" * 50)
        # print(item)
        # with open("iaai.text", "a") as f:
        #     f.write(str(item) + "\n")
        # print("=" * 50)
        yield item

    def get_currency(self, currency):
        if "usd" in currency or "$" in currency:
            return "USD"
        elif "aed" in currency or "AED" in currency:
            return "AED"
        else:
            return ""

    def get_prop(self, response, prop):
        for each in response.css(".data-list.data-list--details")[10].css("li"):
            if each.css("span")[0].css("::text").extract()[0] == (prop):
                return (
                    "".join(each.css("span")[1].css("::text").extract())
                    .replace(" ", "")
                    .replace("\r", "")
                    .replace("\n", "")
                )

        for each in response.css(".data-list.data-list--details")[9].css("li"):
            try:
                if each.css("span")[0].css("::text").extract()[0] == (prop):
                    return (
                        "".join(each.css("span")[1].css("::text").extract())
                        .replace(" ", "")
                        .replace("\r", "")
                        .replace("\n", "")
                    )
            except:
                pass

        try:
            for each in response.css(".data-list.data-list--details")[12].css("li"):
                if each.css("span")[0].css("::text").extract()[0] == (prop):
                    if prop == "Auction Date and Time:":
                        try:
                            t = (
                                "".join(
                                    each.css(":nth-child(2)").css("::text").extract()
                                )
                                .replace(" ", "")
                                .replace("\r", "")
                                .replace("\n", "")
                            )
                            t = t.split(",")[1]
                            t = t.split("(")[0]
                            hours = t.split(":")[0]
                            if len(hours) < 2:
                                t = "0" + t
                            t = self._12hourtime_to_24hourtime(t)
                            t = (str)(t) + ":00"
                            dt = (
                                each.css(":nth-child(2)")
                                .css("::attr(href)")
                                .get()
                                .split("/")[3]
                            )
                            auction_date = datetime.datetime.strptime(
                                dt[4:8] + "-" + dt[0:2] + "-" + dt[2:4] + " " + t,
                                "%Y-%m-%d %H:%M:%S",
                            )
                            return auction_date
                        except:
                            pass
                    elif prop == "Current Bid:":
                        bid = (
                            "".join(each.css(":nth-child(2)").css("::text").extract())
                            .replace(" ", "")
                            .replace("\r", "")
                            .replace("\n", "")
                        )
                        bid = re.search(
                            "(?P<currency>[a-z A-Z $]+)(?P<price>[0-9]+)", bid
                        )
                        return bid
                    else:
                        return (
                            "".join(each.css(":nth-child(2)").css("::text").extract())
                            .replace(" ", "")
                            .replace("\r", "")
                            .replace("\n", "")
                        )
        except:
            pass

        for each in response.css(".data-list.data-list--details")[11].css("li"):
            if each.css("span")[0].css("::text").extract()[0] == (prop):
                if prop == "Auction Date and Time:":
                    try:
                        t = (
                            "".join(each.css(":nth-child(2)").css("::text").extract())
                            .replace(" ", "")
                            .replace("\r", "")
                            .replace("\n", "")
                        )
                        t = t.split(",")[1]
                        t = t.split("(")[0]
                        hours = t.split(":")[0]
                        if len(hours) < 2:
                            t = "0" + t
                        t = self._12hourtime_to_24hourtime(t)
                        t = (str)(t) + ":00"
                        dt = (
                            each.css(":nth-child(2)")
                            .css("::attr(href)")
                            .get()
                            .split("/")[3]
                        )
                        auction_date = datetime.datetime.strptime(
                            dt[4:8] + "-" + dt[0:2] + "-" + dt[2:4] + " " + t,
                            "%Y-%m-%d %H:%M:%S",
                        )
                        return auction_date
                    except:
                        pass
                elif prop == "Current Bid:":
                    bid = (
                        "".join(each.css(":nth-child(2)").css("::text").extract())
                        .replace(" ", "")
                        .replace("\r", "")
                        .replace("\n", "")
                    )
                    bid = re.search("(?P<currency>[a-z A-Z $]+)(?P<price>[0-9]+)", bid)
                    return bid
                else:
                    return (
                        "".join(each.css(":nth-child(2)").css("::text").extract())
                        .replace(" ", "")
                        .replace("\r", "")
                        .replace("\n", "")
                    )

        return ""

    def _12hourtime_to_24hourtime(self, time):
        if time[-2:] == "am":
            if time[:2] == "12":
                time = str("00" + time[2:5])
            else:
                time = time[:-2]
        else:
            if time[:2] == "12":
                time = time[:-2]
            else:
                time = str(int(time[:2]) + 12) + time[2:5]

        return time
