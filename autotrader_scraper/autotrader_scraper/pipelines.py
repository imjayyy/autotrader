from fake_useragent import UserAgent
from scrapy import Request
from scrapy.utils import spider

from car_details.models import *
import json
from items import *
import datetime
from requests_html import HTMLSession
from auction.models import Cities
from us_cities import cities as us_cities

try:
    from autotrader_scraper.autotrader_scraper.middlewares import PROXY_IP
except ImportError:
    from middlewares import PROXY_IP
import logging

logger = logging.getLogger(__name__)


class AddImages:
    def __init__(self):
        pass

    def process_item(self, item, spider=None):
        id = item["LotId"]
        session = HTMLSession()
        r = session.get(
            f"https://www.copart.com/public/data/lotdetails/solr/lotImages/{id}/USA",
            proxies={"http": PROXY_IP},
        )

        item["Images"] = {"FULL_IMAGE": []}

        try:
            images = json.loads(r.text)
            if "data" in images.keys():
                if "imagesList" in images["data"].keys():
                    item["Images"] = images["data"]["imagesList"]
        except:
            pass

        return item


class AdditionalInfo:
    def process_item(self, item, spider=None):
        if type(item) == Auction:
            id = item["LotId"]
            session = HTMLSession()
            # retry to get the additional data with different user agents
            for i in range(25):
                try:
                    r = session.get(
                        f"https://www.copart.com/public/data/lotdetails/solr/{id}",
                        proxies={"http": PROXY_IP, "https": PROXY_IP},
                        headers={
                            'Authority': 'www.copart.com',
                            'Content-Type': 'application/json',
                            'User-Agent': UserAgent().random,
                        }
                    )
                    if json.loads(r.text):
                        break
                except:
                    try:
                        r = session.get(
                            f"https://www.copart.com/public/data/lotdetails/solr/{id}",
                            proxies={"http": PROXY_IP, "https": PROXY_IP},
                                    )
                        if json.loads(r.text):
                            break
                    except:
                        pass

            item["Color"] = None
            item["Transmission"] = None
            item["Drive"] = None
            item["VehicleType"] = None
            item["Cylinders"] = None
            item["Fuel"] = None
            item["Keys"] = None

            try:
                info = json.loads(r.text)
                info["data"]["lotDetails"] = self.model_response_additional_info(
                    info["data"]["lotDetails"]
                )
                item["Color"] = info["data"]["lotDetails"]["clr"]
                item["VehicleType"] = info["data"]["lotDetails"]["vehTypDesc"]
                item["Transmission"] = info["data"]["lotDetails"]["tsmn"]
                item["Cylinders"] = info["data"]["lotDetails"]["cy"]
                item["Fuel"] = info["data"]["lotDetails"]["ft"]
                item["Keys"] = info["data"]["lotDetails"]["hk"]
                item["Drive"] = info["data"]["lotDetails"]["drv"]
            except Exception as e:
                logger.error(e)

        return item

    def model_response_additional_info(self, response):
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

# class AdditionalInfo:
#     def process_item(self, item, spider=None):
#         if isinstance(item, Auction):
#             id = item["LotId"]
#             headers = {
#                 'Authority': 'www.copart.com',
#                 'Content-Type': 'application/json',
#                 'User-Agent': UserAgent().random
#             }
#             url = f"https://www.copart.com/public/data/lotdetails/solr/{id}"
#
#             return Request(
#                 url,
#                 headers=headers,
#                 meta={"item": item},
#                 callback=self.parse_additional_info
#             )
#
#         return item
#
#     def parse_additional_info(self, response):
#         item = response.meta["item"]
#
#         try:
#             info = json.loads(response.body)
#             info["data"]["lotDetails"] = self.model_response_additional_info(
#                 info["data"]["lotDetails"]
#             )
#             item["Color"] = info["data"]["lotDetails"]["clr"]
#             item["VehicleType"] = info["data"]["lotDetails"]["vehTypDesc"]
#             item["Transmission"] = info["data"]["lotDetails"]["tsmn"]
#             item["Cylinders"] = info["data"]["lotDetails"]["cy"]
#             item["Fuel"] = info["data"]["lotDetails"]["ft"]
#             item["Keys"] = info["data"]["lotDetails"]["hk"]
#             item["Drive"] = info["data"]["lotDetails"]["drv"]
#         except Exception as e:
#             spider.logger.error(e)
#
#         return item
#
#     def model_response_additional_info(self, response):
#         keys = [
#             "gr",
#             "al",
#             "aan",
#             "orr",
#             "clr",
#             "vehTypDesc",
#             "ad",
#             "tsmn",
#             "cy",
#             "ft",
#             "hk",
#             "drv",
#         ]
#         for key in keys:
#             if key not in response.keys():
#                 response[key] = None
#         return response


class SaveData:
    def search_in_us_cities(self, name):
        for city in us_cities:
            if city.lower() in name.lower():
                return True
        return False

    def process_item(self, item, spider=None):
        try:
            data = {
                "lotId": item["LotId"],
                "year": item["Year"],
                "make": item["Make"],
                "modelGroup": item["ModelGroup"],
                "model": item["Model"],
                "bodyStyle": item["BodyStyle"],
                "color": item["Color"],
                "primaryDamage": item["PrimaryDamage"],
                "vin": item["Vin"],
                "odometer": item["Odometer"],
                "engineSize": item["EngineSize"],
                "locationName": item["LocationName"],
                "vehicleType": item["VehicleType"],
                "imageFull": item["ImageFull"],
                "imageThumb": item["ImageThumb"],
                "vinHash": item["VinHash"],
                "saledate": item["SaleDate"],
                "searchTerm": item["SearchTerm"],
                "dateCreated": item["DateCreated"],
                "transmission": item["Transmission"],
                "keys": item["Keys"],
                "cylinders": item["Cylinders"],
                "drive": item["Drive"],
                "fuel": item["Fuel"],
                "secondaryDamage": item["SecondaryDamage"],
                "odometerType": item["OdometerType"],
                "auctionCompanyId": item["AuctionCompanyId"],
                "buyItNow": item.get("BuyItNow"),
            }

            time = datetime.datetime.now()

            if type(data["dateCreated"]) != type(time):
                data["dateCreated"] = None
            if type(data["saledate"]) != type(time):
                data["saledate"] = None

            if not LotData.objects.filter(lotId=item["LotId"]).exists():
                lot_data = LotData(**data)
                lot_data.save()

        except Exception as e:
            logger.error(e)
            pass

        try:
            data = {
                "LotId": item["LotId"],
                "BidStatus": item["BidStatus"],
                "SaleStatus": item["SaleStatus"],
                "CurrentBid": item["CurrentBid"],
                "Currency": item["Currency"],
            }

            bid_information = BidInformation(**data)
            bid_information.save()
            data = {
                "LotId": item["LotId"],
                "Lane": item["Lane"],
                "Item": item["Item"],
                "Grid": item["Grid"],
                "LastUpdated": item["LastUpdated"],
            }

            sale_information = SaleInformation(**data)
            sale_information.save()
        except Exception as e:
            pass

        try:
            for image in item["Images"]["FULL_IMAGE"]:
                lot_id = item["LotId"]
                url = image["url"]
                check_for_existing_images = LotImages.objects.filter(
                    LotId=lot_id, ImageFull=url
                )
                data = {"LotId": lot_id, "ImageFull": url}
                if len(check_for_existing_images) > 0:
                    data["Id"] = check_for_existing_images[0].Id

                lot_images = LotImages(**data)
                lot_images.save()
        except Exception as e:
            pass

        return item
