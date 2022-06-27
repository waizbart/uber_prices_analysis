import requests
import json
from pprint import pprint
from dotenv import dotenv_values
from time import sleep
import csv
from datetime import datetime
import pyowm

env = dotenv_values(".env")

owm = pyowm.OWM(env["API_KEY"])
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Sorocaba,BR')
weather = observation.weather

file_csv = open('uber_prices_data.csv', 'w', newline='', encoding='utf-8')
write_csv = csv.writer(file_csv)

headers = {
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-csrf-token": "x",
    "x-uber-wa-info": "KJFFQQKPSQNQPRPRQQIGPTNS",
    "cookie": env["COOKIE"],
    "Referrer-Policy": "strict-origin-when-cross-origin",
}

body = '{"operationName": "FareEstimate", "variables": {"destination": {"latitude": -23.4493531, "longitude": -47.3639386}, "pickupLocation": {"latitude": -23.4678406, "longitude": -47.438954}, "vehicleViewIds": [11803, 20022265, 20034913], "synced": true}, "query": "query FareEstimate($pickupLocation: InputLocation!, $destination: InputLocation, $pickupTimeMS: Float, $targetProductType: EnumTargetProductType, $vehicleViewIds: [Int!]!) {\\n  fareEstimate(pickupLocation: $pickupLocation, destination: $destination, pickupTimeMS: $pickupTimeMS, targetProductType: $targetProductType, vehicleViewIds: $vehicleViewIds) {\\n    ...FareEstimateFragment\\n    __typename\\n  }\\n}\\n\\nfragment FareEstimateFragment on FareEstimateReturn {\\n  fares\\n  vehicleViewsOrder\\n  __typename\\n}\\n"}'

while True:
    try:
        req = requests.post("https://m.uber.com/graphql",
                            headers=headers, data=body)

        json = req.json()

        fares = json["data"]["fareEstimate"]["fares"]

        row = []

        for key in fares:
            element = fares[key] 

            if key == "20022235":
                row.append(fares[key]["fare"].replace("R$", ""))

            if key == "20030105":
                row.append(fares[key]["fare"].replace("R$", ""))

            if key == "20037953":
                row.append(fares[key]["fare"].replace("R$", ""))

        row.append(datetime.now())
        row.append(weather.detailed_status)
        row.append(weather.temperature('celsius')['temp'])
        write_csv.writerow(row)

        sleep(5)

    except KeyboardInterrupt:
        write_csv.close() 
        break

    except Exception as e:
        print(e)
        continue

    
