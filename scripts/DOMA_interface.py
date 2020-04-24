import json


class DOMA:
    def __init__(self:):


    def edit_json(self, newFlight):
        # we try to write an existing json. If not existing, we create a new one
        try:
            with open('/home/pi/Desktop/HF-LOCUST-WASP/DOMA.json', 'r+') as f:
                data = []
                try:
                    data = json.load(f)
                except:
                    print("Empty json r+")

                data.append(newFlight)
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

                data.append(newFlight)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                f.close()


    def write_json(self, timestamp, num, percentage, data_drone, image_settings, path):
        coordinates = (data_drone[0], data_drone[1])
        self.results.append(
            {
                "image_id": num,
                "percentage": percentage,
                "coordinates": coordinates,
                "image_path": path,
                "camera_settings": image_settings,
            }
        )

        flight = {
            "id": timestamp,
            "flight_data": self.results
        }

        return flight