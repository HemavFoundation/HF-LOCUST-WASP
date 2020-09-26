from config import *
import numpy as np
import json
import reverse_geocoder as rg
import time

class DataManagement():
    def __init__(self):
        self.mission_type = typeOfMission
        
        self.results = []
        self.visualimages = []
        self.flights = []
        
        self.flight_time = None
        self.flight_start = time.perf_counter()

        self.home_coordinates = home_coordinates
        self.region, self.country = self.location_decoder(home_coordinates)

        self.flights.append(
            "id_plate": drone_id,
            "id_flight": timestamp,
            "typeOfFlight": typeOfMission,
            "homeCoordinates": home_coordinates, 
            "country": self.country,
            "region": self.region,
            "date": ,
            "flightTime": self.flight_time,
            "GreenResults": self.results,
            "VisualImages": self.visualimages,
        )

        flights_information = {
            "dataOfFlights": self.flights,
        }


    def edit_json(self, new_flight):

        self.flight_time = time.perf_counter() - self.flight_start

        # we try to write an existing json. If not existing, we create a new one
        try:
            with open('/home/pi/Desktop/HF-LOCUST-WASP/results.json', 'r+') as f:
                data = []
                try:
                    data = json.load(f)
                except:
                    print("Empty json r+")

                data.append(new_flight)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                f.close()

        except:
            with open('/home/pi/Desktop/HF-LOCUST-WASP/results.json', 'w') as f:
                data = []
                try:
                    data = json.load(f)
                except:
                    print("Empty json x")

                data.append(new_flight)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                f.close()

        print("done")

    def write_json_vegetation(self, timestamp, num, percentage, data_drone, path):
        
        coordinates = (data_drone[0], data_drone[1])
        
        self.results.append(
            {
                "image_id": num,
                "percentage": percentage,
                "coordinates": coordinates,
                "image_path": path,
            }
        )

        flight = {
            "dataOfFlights": self.flights,
        }

        return flight

    def write_json_visual(self, timestamp, num_visual, path_visual):

        self.visualimages.append(
            {
                "image_id": num_visual,
                "image_path": path_visual,
            }
        )

        flight = {
            "dataOfFlights": self.flights,
        }

        return flight
    
    def location_decoder(self, coordinates):  # function to know the region and the country where the flight takes place
        location = rg.search(coordinates)

        df = pd.DataFrame.from_dict(location)
        region = df['name'][0]
        state = df['admin1'][0]
        country = df['cc'][0]

        return region, country






