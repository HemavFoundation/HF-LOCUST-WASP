import json


class DOMA():
    def __init__(self):
        self.drone_plate = 'HP2_FAO_078'


        #We initialize some other variables that has nothing related with camera settings

        self.flights_info = []

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


    def write_json(self, timestamp,):
        coordinates = (data_drone[0], data_drone[1])
        self.flights_info.append(
            {
                "date": 
                "time": 
                "country": 
                "region": 
                "flight type":
                "flight time": 
            }
        )

        drone_info = {
            "id": self.drone_plate,
            "flight_data": self.flights_info
        }

        return drone_info