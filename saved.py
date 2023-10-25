


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
