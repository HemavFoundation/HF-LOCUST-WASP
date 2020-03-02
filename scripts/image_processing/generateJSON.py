import json
import pandas as pd

def edit_json(newFlight):
    try:
        with open('C:/Users/anavarrete/Desktop/results/endurance flight/results.json', 'r+') as f:
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
        with open('C:/Users/anavarrete/Desktop/results/endurance flight/results.json', 'w') as f:
            data = []
            try:
                data = json.load(f)
            except:
                print("Empty json a")
            data.append(newFlight)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()
    print("done")

def write_json(timestamp, num, image_path):
    results.append(
        {
                "image_id": num,
                "image_path": image_path,
            }
    )
    flight = {
        "id": timestamp,
        "results": results
    }
    return flight

# Declare variables
date = pd.datetime.now().date()
hour = pd.datetime.now().hour
minute = pd.datetime.now().minute
seconds = pd.datetime.now().second

num = 1
i = 0
timestamp = str(hour) + '/' + str(minute)
flight_info = None
results = []
while i < 100:
    timestamp = 'Test Flight'
    image_path = 'C:/Users/anavarrete/Desktop/results/endurance flight/raw_images' + '/' + str(num) + '.jpeg'
    flight_info = write_json(timestamp, num, image_path)
    num += 1 
    i += 1

if flight_info is not None:
    try:
        edit_json(flight_info)
    except:
        print("No flight")
else:
    print('no funciona')