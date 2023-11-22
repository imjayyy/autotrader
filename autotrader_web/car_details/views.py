from django.views.generic.base import TemplateView
from auction.models import Cities, AuctionShipping, AuctionCompany, ShippingCompany, ShippingAuctionFee
from .models import *
from django.shortcuts import redirect, render
import datetime
from datetime import timezone
from myroot.languages import languages
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class CarDetailsView(TemplateView):
    template_name = 'auction/car-details.html'

    def get_lot_information(self, lot, lang):
        KOREAN_LOT, SCRAPED_LOT = False, False

        if LotData.objects.filter(lotId=lot).exists():
            SCRAPED_LOT = True
            lot_data_model = LotData.objects.filter(lotId=lot)[0]
        elif KoreanLot.objects.filter(Id=lot).exists():
            KOREAN_LOT = True
            lot_data_model = KoreanLot.objects.filter(Id=lot)[0]

        if KOREAN_LOT:
            images = lot_data_model.Images.all()
            final_images = []
            imgid = 0

            for image in images:
                final_images.append({
                    "thumbnail": "/static/uploads/" + image.Image.name,
                    "full": "/static/uploads/" + image.Image.name,
                    "hdr": "/static/uploads/" + image.Image.name,
                    "id": imgid
                })
                imgid += 1

            return {
                "exists": True,
                "images": final_images,
                "lotId": lot_data_model.Id,
                "details_array": [
                    {"key": lang["vin"], "value": lot_data_model.Vin},
                    {"key": lang["odometer"], "value": lot_data_model.Odometer},
                    {"key": lang["body_style"], "value": lot_data_model.BodyStyle},
                    {"key": lang["color"], "value": lot_data_model.Color},
                    {"key": lang["engine"], "value": lot_data_model.Engine},
                    {"key": lang["transmission"], "value": lot_data_model.Transmission},
                    {"key": lang["drive"], "value": lot_data_model.Drive},
                    {"key": lang["fuel"], "value": lot_data_model.FuelType.NameEn},
                    {"key": lang["year"], "value": lot_data_model.Year},
                    {"key": lang["price"], "value": lot_data_model.Price},
                ]
            }

        elif SCRAPED_LOT:
            auction_company = AuctionCompany.objects.get(Id=lot_data_model.auctionCompanyId)

            images = lot_data_model.LotImages
            final_images = []
            imgid = 0

            for image in images:
                final_images.append({
                    "thumbnail": image.ImageFull,
                    "full": image.ImageFull,
                    "hdr": image.ImageFull,
                    "id": imgid
                })
                imgid += 1

            if lot_data_model.saledate is not None:
                time_left = lot_data_model.saledate - datetime.datetime.now(timezone.utc)

                time_left = {
                    "d": time_left.days,
                    "h": time_left.seconds // 3600,
                    "m": (time_left.seconds // 60) % 60,
                    "time_crossed": False
                }

                if datetime.datetime.now(timezone.utc) > lot_data_model.saledate:
                    time_left["time_crossed"] = True

            else:
                time_left = {
                    "d": None,
                    "h": None,
                    "m": None,
                    "time_crossed": False
                }
            print(lot_data_model.locationName, '-----------------------------------------------')

            # try:
            #     if ' - ' in lot_data_model.locationName:
            #         loc = lot_data_model.locationName.split(' - ')
            #         city = Cities.objects.filter(Name__icontains=loc[1])[0]
            #     else:
            #         city = Cities.objects.filter(Name__icontains=lot_data_model.locationName)[0]
            #     location_city = city.Name
            #     location_state = city.State
            #     location_port = city.Port
            #     country = city.Country
            # except Exception as e:
            #     try:
            #         if ' - ' in lot_data_model.locationName:
            #             loc = lot_data_model.locationName.split(' - ')
            #             city = Cities()
            #             city.Name = loc[1]
            #             city.State = loc[0]
            #             city.Port = loc[0]
            #             city.Country = 'US'
            #             city.save()
            #             location_city = city.Name
            #             location_state = city.State
            #             location_port = city.Port
            #             country = city.Country
            #     except:
            #         location_city = lot_data_model.locationName
            #         location_state = "N/A"
            #         country = "N/A"
            #         location_port = "N/A"
            city = Cities.objects.filter(Name__icontains=lot_data_model.locationName)[0]
            location_city = city.Name
            location_state = city.State
            location_port = city.Port
            country = city.Country




            try:
                large_image = final_images[0]["full"] if len(final_images) >= 1 else None
            except Exception as e:
                large_image = None

            data = {
                "details_array": [
                    {"key": lang["vin"], "value": lot_data_model.vin},
                    # {"key": "titleCode", "value": None},
                    {"key": lang["odometer"], "value": lot_data_model.odometer},
                    {"key": lang["primary_damage"], "value": lot_data_model.primaryDamage},
                    {"key": lang["secondary_damage"], "value": lot_data_model.secondaryDamage},
                    {"key": lang["body_style"], "value": lot_data_model.bodyStyle},
                    {"key": lang["color"], "value": lot_data_model.color},
                    {"key": lang["engine"], "value": lot_data_model.engineSize},
                    {"key": lang["cylinders"], "value": lot_data_model.cylinders},
                    {"key": lang["transmission"], "value": lot_data_model.transmission},
                    {"key": lang["drive"], "value": lot_data_model.drive},
                    {"key": lang["fuel"], "value": lot_data_model.fuel},
                    {"key": lang["keys"], "value": lot_data_model.keys},
                    {"key": lang["special_note"], "value": "N/A"},
                ],
                "exists": True,
                "lotId": lot_data_model.lotId,
                "vehicleType": lot_data_model.vehicleType,
                "year": lot_data_model.year, "make": lot_data_model.make, "modelGroup": lot_data_model.modelGroup,
                "model": lot_data_model.model, "bodyStyle": lot_data_model.bodyStyle, "color": lot_data_model.color,
                "primaryDamage": lot_data_model.primaryDamage,
                "vin": lot_data_model.vin,
                "odometer": lot_data_model.odometer, "engineSize": lot_data_model.engineSize,
                "minimumBid": None, "currency": lot_data_model.BidInformation.Currency,
                "saleLocation": {"port":location_port,"name": location_city, "state": location_state, "country": country},
                "saleDate": lot_data_model.saledate,
                "item": lot_data_model.SaleInformation.Item, "gridRow": lot_data_model.SaleInformation.Grid,
                "lastUpdatedAt": lot_data_model.SaleInformation.LastUpdated,
                "largeImage": large_image,
                "lane": lot_data_model.SaleInformation.Lane,
                "images": final_images,
                "currentBid": lot_data_model.BidInformation.CurrentBid,
                "transmission": lot_data_model.transmission,
                "drive": lot_data_model.drive,
                "keys": lot_data_model.keys,
                "fuel": lot_data_model.fuel,
                "cylinders": lot_data_model.cylinders,
                "specialNote": "N/A",
                "secondaryDamage": lot_data_model.secondaryDamage,
                "suggestedBid": "N/A",
                "odometerType": lot_data_model.odometerType,
                "auctionHighlights": None,
                "titleCode": None,
                "saleStatus": lot_data_model.BidInformation.SaleStatus,
                "bidStatus": lot_data_model.BidInformation.BidStatus,
                "timeLeft": time_left,
                "sellerReserve": None,
                "auctionCompany": auction_company.Name
            }

            if data["engineSize"] == "UNKNOWNSPECS":
                data["engineSize"] = ""

            return data
        else:
            return {"exists": False}

    def get_similar_vehicles(self, context):
        try:
            model = context["data"]["model"]
            make = context["data"]["make"]
            cars = LotData.objects.filter(model=model, make=make)
            cars = cars.filter(~Q(id=context.get("data").get("id")))
            context["cars"] = cars
            for key in context["data"].keys():
                if context["data"][key] is None or context["data"][key] == "":
                    context["data"][key] = "N/A"

            cars_modified = []
            for car in context["cars"]:
                car_mod = {
                    "lotId": car.lotId,
                    "saledate": car.saledate,
                    "BidInformation": car.BidInformation,
                    "locationName": car.locationName,
                    "odometer": car.odometer,
                    "odometerType": car.odometerType,
                    "year": car.year,
                    "model": car.model,
                    "make": car.make,
                    "images": []
                }
                img_id = 0
                for img in car.LotImages:
                    car_mod["images"].append({
                        "ImageFull": img.ImageFull,
                        "Id": img_id
                    })
                    img_id += 1
                cars_modified.append(car_mod)

            context["cars"] = cars_modified[0:5]
        except Exception as e:
            logger.error(e)
        return context


    def get_context_data(self, lang):
        context = {"data": self.get_lot_information(self.kwargs["id"], lang)}
        context["lang"] = lang
        context = self.get_similar_vehicles(context)
        return context

    def translate_props(self, context):
        try:
            props_to_translate = ["transmission", "vehicleType", "bodyStyle", "primaryDamage", "secondaryDamage",
                                  "odometerType", "color", "drive", "fuel", "keys"]

            for prop in props_to_translate:
                context["data"][prop] = context["lang"].get(context["data"][prop])
                if context["data"][prop] is None:
                    context["data"][prop] = ""
        except:
            pass

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(languages[request.lang])

        if not context["data"]["exists"]:
            return redirect('/')

        context = self.translate_props(context)
        response = render(request, self.template_name, context)

        return response
