from config import *
import numpy as np
import json



class DataManagement():
    def __init__(self):
        self.mission_type = typeOfMission
       
        self.results = []
        self.visualimages = []

    def edit_json(self, new_flight):
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
            "id": timestamp,
            "typeOfFlight": self.mission_type,
            "GreenResults": self.results,
            "VisualImages": self.visualimages,
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
            "id": timestamp,
            "typeOfFlight": self.mission_type,
            "GreenResults": self.results,
            "VisualImages": self.visualimages,
        }

        return flight





