import requests, json
import pyodbc
from datetime import datetime, timedelta
# Replace with your API token
api_token = "6394dc91ece3542af402645dc9f2aa1b2c2dec923b24cf3d249373228a019684"


def save_to_db():
      # Define your database connection details
      server = 'localhost'
      database = 'AutoTrader_Db'
      username = 'SA'
      password = 'Pakistan1'
      json_file_path = 'path_to_your_json_file.json'

      # Establish a connection to the SQL Server
      connection_string = f'DRIVER=ODBC Driver 18 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=no;TrustServerCertificate=yes;'
      connection = pyodbc.connect(connection_string)

      # Create a cursor for executing SQL queries
      cursor = connection.cursor()
      print("connected to DB" )
      # try:
      # Read data from the JSON file
      with open("response2.json", 'r') as json_file:
          data = json.load(json_file)['result']
      
      
      
      # data = json_data
      # Assuming the JSON data is a list of records, you can iterate through it and insert each record into the database
      try:
          for json_data in data:
            # Define your SQL query
            searchTerm = str(json_data["make"]) + " " + str(json_data["model"]) + " " + str(json_data["body_style"])
            odometerType = "Actual"
            # Construct the modelGroup
            modelGroup = ""
            if len(json_data["sales_history"]) > 0 :              
              sales_history = json_data["sales_history"][0]["sale_date"] 
              sales_history = datetime.utcfromtimestamp(int(sales_history) / 1000) 
            else:
              sales_history = None

            if json_data["buy_now_car"]["auction_name"] ==  "COPART":
              auctionCompanyId = 1
            if json_data["buy_now_car"]["auction_name"] ==  "IAAI":
              auctionCompanyId = 2
            location_ = json_data["location"]
            if '-' in location_ :
               location_ = location_.split(' - ')[1]
            
            sql_query = """
            INSERT INTO [LotData] (
                [modelGroup], [lotId], [year], [make], [model], [bodyStyle], [color], [primaryDamage],
                [vin], [odometer], [engineSize], [locationName], [vehicleType], [imageFull], [imageThumb], [vinHash],
                [saledate], [searchTerm], [dateCreated], [transmission], [drive], [cylinders], [fuel], [keys],
                [secondaryDamage], [odometerType], [auctionCompanyId], [buyItNow]
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """

            # Execute the SQL query with parameters
            cursor.execute(
                sql_query,
                (
                    modelGroup, json_data["id"], json_data["year"], json_data["make"], json_data["model"],
                    json_data["body_style"], json_data["color"], json_data["primary_damage"], json_data["vin"],
                    json_data["odometer"], json_data["engine_type"], location_, json_data["vehicle_type"],
                    json_data["car_photo"]["photo"][0] if "car_photo" in json_data else None,
                    json_data["car_photo"]["photo"][0] if "car_photo" in json_data else None, "---",
                    sales_history,
                    searchTerm, datetime.now(), json_data["transmission"], json_data["drive"], json_data["cylinders"],
                    json_data["fuel"], json_data["car_keys"], json_data["secondary_damage"], odometerType,
                    auctionCompanyId, json_data["buy_now_car"]["purchase_price"] if "buy_now_car" in json_data else None
                )
            )
            for photo_url in json_data['car_photo']['photo']:
              cursor.execute(
                  "INSERT INTO [LotImages] ([LotId], [ImageFull]) VALUES (?, ?)",
                  (json_data['car_photo']['all_lots_id'], photo_url)
              )
            connection.commit()
            print("Data inserted successfully.")
      except Exception as e:
         print('Error', e)
         print(json_data)
      finally:
          # Close the cursor and the database connection
          cursor.close()
          connection.close()
      

def fetch_data():
  url = "https://api.copart-iaai-api.com/api/v2/get-cars"
  headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json",
      "Api-Version": "V2",
  }

  today = datetime.now()
  previous_day = today - timedelta(days=1)
  three_weeks_from_today = today + timedelta(weeks=3)
  previous_day_str = previous_day.strftime("%Y-%m-%d")
  three_weeks_from_today_str = three_weeks_from_today.strftime("%Y-%m-%d")
  current_year = datetime.now().year

  # Subtract 10 years
  result_year = current_year - 10
  # Define the query parameters
  params = {
      "make": "BMW",
      "year_from" : str(result_year),
      "page": "1",
      "per_page": "80",
      'auction_date_from': previous_day_str,
      'auction_date_to': three_weeks_from_today_str,
      "api_token": api_token,
  }
  data = {}

  response = requests.post(url, headers=headers, params=params)

  if response.status_code == 200:
      # Request was successful

      response_data = response.json()
      # save_to_db( response_data['result'] )
      # Save response to a JSON file
      with open("response2.json", "w") as json_file:
          json.dump(response_data, json_file, indent=4)
  else:
      # Request failed
      print(f"Request failed with status code {response.status_code}: {response.text}")



# save_to_db()
fetch_data()
