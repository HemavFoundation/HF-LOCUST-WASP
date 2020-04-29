import json
import reverse_geocoder as rg
import numpy as np
import pandas as pd
from time import time
import datetime


class DOMA():
    def __init__(self):
        self.drone_plate = 'HP2_FAO_078'


        #We need to initialize some variables that will be used later on

        self.flights_info = []
        self.flight_timer = 0

    def edit_json(self, DOMA_input):
        # we try to write an existing json. If not existing, we create a new one
        try:
            with open('/home/pi/Desktop/HF-LOCUST-WASP/DOMA.json', 'r+') as f:
                data = []
                try:
                    data = json.load(f)
                except:
                    print("Empty json r+")

                data.append(DOMA_input)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                f.close()

        except:
            with open('/home/pi/Desktop/HF-LOCUST-WASP/DOMA.json', 'w') as f:
                data = []
                try:
                    data = json.load(f)
                except:
                    print("Empty json x")

                data.append(DOMA_input)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                f.close()


    def write_json(self, timestamp, data_drone, mission_type, flight_duration):
        coordinates = (data_drone[0], data_drone[1])

        region, country = location_decoder(coordinates)

        self.flights_info.append(
            {
                "date": 
                "time": 
                "country": country
                "region": region
                "flight type": mission_type
                "flight time": flight_duration
            }
        )

        drone_info = {
            "id": self.drone_plate,
            "flight_data": self.flights_info
        }

        return drone_info
    
    def location_decoder(self, coordinates):  # function to know the region and the country where the flight takes place
        location = rg.search(coordinates)

        df = pd.DataFrame.from_dict(location)
        region = df['name'][0]
        state = df['admin1'][0]
        country = df['cc'][0]

        return region, country

    
    def start_flight(self):
        self.flight_timer = time.time()


    def end_flight(self):
        duration = time.time() - self.flight_timer

        flight_duration = datetime.timedelta(seconds = duration)

        return str(flight_duration)
    
