import json, requests
from car_details.models.lot_data import LotData
from car_details.models.bid_information import BidInformation
from car_details.models.lot_images import LotImages
from car_details.models.sale_information import SaleInformation
from car_details.models.brand import Brand

from datetime import datetime, timedelta



api_token = "6394dc91ece3542af402645dc9f2aa1b2c2dec923b24cf3d249373228a019684"

class Db_updater():
    def __init__(self) -> None:
        # LotData.delete(self)
        pass


    def process_data(self, item):
        item["lot_number"] = int(item["lot_number"])
        dt = None
        if len(item["active_bidding"]) > 0:
            if item['active_bidding'][0]["sale_date"] :
                dt = datetime.utcfromtimestamp(int(item["active_bidding"][0]["sale_date"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')   
        loc = loc = item["location"].split(' - ')[1].lower() if item.get("location") and ' - ' in item["location"] else item.get("location")
        self.loddata_data = {
            "lotId": int(item["lot_number"]),
            "year": item["year"],
            "make": item["make"],
            "modelGroup": "",
            "model": item["model"],
            "bodyStyle": item["body_style"],
            "color": item["color"],
            "primaryDamage": item["primary_damage"],
            "vin": item["vin"],
            "odometer": item["odometer"],
            "engineSize": item["engine_type"],
            "locationName": loc,
            "vehicleType": item["vehicle_type"],
            "imageFull": item["car_photo"]['photo'][0] if len(item["car_photo"]['photo']) > 0 else None,
            "imageThumb": item["car_photo"]['photo'][0] if len(item["car_photo"]['photo']) > 0 else None,
            "vinHash": '',
            "saledate": dt ,
            "searchTerm": str(item["make"]) + " " + str(item["model"]) + " " + str(item["body_style"]), 
            "dateCreated": datetime.now(),
            "transmission": item["transmission"],
            "keys": item["car_keys"],
            "cylinders": item["cylinders"],
            "drive": item["drive"],
            "fuel": item["fuel"],
            "secondaryDamage": item["secondary_damage"],
            "odometerType": "Actual",
            "auctionCompanyId": 1 if item["auction_name"] ==  "COPART" else 2,
            "buyItNow": 1 if item["buy_now_car"] else 0,
        }

        self.bid_information_data = {
            "LotId": item["lot_number"],
            "BidStatus": None,
            "SaleStatus": None,
            "CurrentBid": item["active_bidding"][0]['current_bid']  if len(item["active_bidding"]) > 0 else None,
            "Currency": "USD",
        }

        self.saleInformation_data = {
            "LotId": item["lot_number"],
            "Lane": None,
            "Item": None,
            "Grid": None,        
            # "Lane": item["Lane"],
            # "Item": item["Item"],
            # "Grid": item["Grid"],
            "LastUpdated": datetime.now(),
        }

        self.lot_images_data = []

        for image in item["car_photo"]['photo']:
            temp_data = {"LotId": item["lot_number"], "ImageFull": image}
            self.lot_images_data.append(temp_data)

    def save_data(self):
        # print(**self.loddata_data)
        lot_data_instance = LotData()
        for field, value in self.loddata_data.items():
            setattr(lot_data_instance, field, value)
        lot_data_instance.save()

        bid_information_instance = BidInformation()
        self.bid_information_data['LotId'] = lot_data_instance
        for field, value in self.bid_information_data.items():
            setattr(bid_information_instance, field, value)
        bid_information_instance.save()


        sale_information_instance = SaleInformation()
        self.saleInformation_data['LotId'] = lot_data_instance
        for field, value in self.saleInformation_data.items():
            setattr(sale_information_instance, field, value)
        sale_information_instance.save()

        for image_data in self.lot_images_data:
            LOT_IMAGES_INSTANCE = LotImages()
            image_data['LotId'] = lot_data_instance
            for field, value in image_data.items():
                setattr(LOT_IMAGES_INSTANCE, field, value)
            LOT_IMAGES_INSTANCE.save()


    def get_data_from_api(self, make:str, con):
        url = "https://api.copart-iaai-api.com/api/v2/get-cars"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Api-Version": "V2",
        }

        today = datetime.now()
        previous_day = today - timedelta(days=2 )
        three_weeks_from_today = today + timedelta(weeks=3)
        previous_day_str = previous_day.strftime("%Y-%m-%d")
        three_weeks_from_today_str = three_weeks_from_today.strftime("%Y-%m-%d")
        current_year = (datetime.now().year)

        # Subtract 10 years
        result_year = current_year - 10
        # Define the query parameters
        params = {
            "make": make,
            "year_from" : str(result_year),
            'year_to': str(current_year),
            "page": "1",
            "per_page": "80",
            'auction_date_from': previous_day_str,
            'auction_date_to': three_weeks_from_today_str,
            "api_token": api_token,
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                # Request was successful
                LotData.objects.filter(make=make).delete()
                response_data = response.json()

                pages = response_data["pagination"]["total_pages"]
                con.send( f"found {pages} pages for the make {make}, total {response_data['pagination']['total']} cars")
                for page in range (1, pages+1):
                    params['page'] = page
                    response = requests.post(url, headers=headers, params=params)
                    response_data = response.json()
                    data = response_data['result']
                    for item in data:
                        try:
                            self.process_data(item)
                            self.save_data()
                        except Exception as e:
                            con.send(str(e) + ' ' + str(make) + ' ' + 'In item')
            except Exception as e:
                con.send( str(e) + ' ' + str(make) )
            # save_to_db( response_data['result'] )
            # Save response to a JSON file
            # with open("response2.json", "w") as json_file:
            #     json.dump(response_data, json_file, indent=4)
        else:
            # Request failed
            con.send(f"Request failed with status code {response.status_code}: {response.text}")

    def update_all(self, con):
        brands = Brand.objects.filter()
        for brand in brands:
            self.get_data_from_api(brand.NameEn, con)
