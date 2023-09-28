import logging

from auction.models import *
from car_details.models import LotData
import requests
import json
import re

import logging

logger = logging.getLogger(__name__)


class AuctionCalculatorService:

    def __init__(self):
        self.Bid = None
        self.Total = None
        self.BakuFee = None
        self.ShippingFee = None
        self.ServiceFee = None
        self.AuctionFee = None
        self.AuctionCompany = None
        self.Country = None
        self.Port = None
        self.Calculated = False
        self.Currency = None
        self.DocumentationFee = None
        self.InsuranceFee = None
        self.CustomsFee = None
        self.TransferFee = None

    def calculate_by_lotid(self, lotid, bid, to_country):
        lot = LotData.objects.get(lotId=lotid)
        auction_company_id = lot.auctionCompanyId
        city_id = Cities.objects.filter(Name__icontains=lot.locationName)
        self.calculate(auction_company_id, bid, city_id[0].Id, to_country)
        try:
            self.set_customs_fee(lot)
        except Exception as e:
            print(f"Customs Fee Calculation Error: {e}")

    def set_customs_fee(self, lot):
        auto_type = "0"

        engine_type_values = {
            "benzin": "0",
            "gasoline": "0",
            "flexiblefuel": "0",
            "unknown": "0",
            "other": "0",
            "dizel": "1",
            "diesel": "1",
            "gas": "2",
            "hybrid benzin": "3",
            "hybrid dizel": "4",
            "electric": "5",
            "compressed natural gas": "0",
            "flexible fuel": "0",
            "hybrid engine": "3",
        }
        engine_type = engine_type_values[lot.fuel.lower()] if lot.fuel.lower() in engine_type_values.keys() else "0"
        engine = float(re.findall('\d+\.\d{0,10}L', lot.engineSize.upper())[0][0:-1]) * 1000
        issue_date = "31.01." + str(lot.year)
        price = self.Bid + self.AuctionFee + self.TransferFee + self.ShippingFee
        data = {
            "commerceType": "0",
            "autoType": auto_type,
            "engineType": engine_type,
            "price": price,
            "engine": int(engine),
            "issueDate": issue_date,
        }

        response = requests.post(
            "https://c2b-fbusiness.customs.gov.az/api/v1/dictionaries/calAutoDuty",
            json=data,
            headers={"Content - Type": "application / json"}
        )
        # Will log to django_errors.log
        print("DEV_CUSTOMS_CALCULATION_CALL_START")
        print(data)
        print(response.text)
        print("DEV_CUSTOMS_CALCULATION_CALL_END")
        self.CustomsFee = round(json.loads(response.text)["data"]["autoDuty"]["total"]["value"] / 1.7, 0)

    def calculate(self, auction_id, bid, city_id, to_country="Georgia", user_types_id=1):
        try:
            max_price = 15000

            user = UserTypes.objects.get(Id=user_types_id)
            auction = AuctionCompany.objects.get(Id=auction_id)
            ship_id = ShippingCompany.objects.filter(Chosen=1)[0].Id

            service_fee = user.ServiceFee
            baku_fee = float(user.ToBakuFee)
            marja = user.Marja
            gate_fee = auction.GateFee
            onlinebid = AuctionOnlinelivebid.objects.filter(StartPrice__lte=bid, EndPrice__gte=bid, AuctionCompanyId=auction_id)[
                0].Fee
            auction_fee = \
                AuctionFee.objects.filter(StartPrice__lte=bid, EndPrice__gte=bid, AuctionCompanyId=auction_id)[0].Fee

            if float(bid) >= max_price:
                auction_fee = float(auction_fee) * float(bid) / 100

            total_auction_fee = float(auction_fee) + float(onlinebid) + float(gate_fee)

            shipping_auction = AuctionShipping.objects.filter(AuctionCompanyId=auction_id, ShippingCompanyId=ship_id)[
                0].Id
            shipping_fee = 0

            if ShippingAuctionFee.objects.filter(AuctionShippingId=shipping_auction, CitiesId=city_id,
                                                 UserTypesId=user_types_id).exists():
                shipping_fee = ShippingAuctionFee.objects.filter(AuctionShippingId=shipping_auction, CitiesId=city_id,
                                                                 UserTypesId=user_types_id)[0].Fee

            if to_country == "Azerbaijan":
                self.TransferFee = baku_fee
            else:
                self.TransferFee = 0

            total_shipping_fee = float(shipping_fee) + float(marja)
            total_fee = float(self.TransferFee) + float(bid) + float(total_shipping_fee) + float(
                total_auction_fee) + float(service_fee)

            self.Total = total_fee
            self.ServiceFee = service_fee
            self.ShippingFee = total_shipping_fee
            self.AuctionFee = total_auction_fee
            self.Bid = float(bid)
            self.BakuFee = baku_fee
            self.Country = Cities.objects.get(Id=city_id).Country
            self.Port = Cities.objects.get(Id=city_id).Port
            self.AuctionCompany = AuctionCompany.objects.get(Id=auction_id).Name
            self.Currency = "USD"
            self.Calculated = True
            self.DocumentationFee = 0
            self.InsuranceFee = 0

        except Exception as e:
            logger.error(e)
            self.Calculated = False

    def json(self):
        if self.Calculated:
            response = {
                "bid": self.Bid,
                "baku_fee": self.BakuFee,
                "shipping_fee": self.ShippingFee,
                "service_fee": self.ServiceFee,
                "auction_fee": self.AuctionFee,
                "currency": self.Currency,
                "auction": self.AuctionCompany,
                "country": self.Country,
                "port": self.Port,
                "transfer_fee": self.TransferFee,
                "insurance_fee": self.InsuranceFee,
                "documentation_fee": self.DocumentationFee,
                "customs_fee": self.CustomsFee,
                "total": self.Total
            }
            return response
        else:
            raise Exception(
                "There was an error parsing the calculation. Please make sure the calculation was performed successfuly")
