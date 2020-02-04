from __future__ import print_function
from dronekit import *
import time
import os
from autopilot_interface import AutopilotInterface
from camera_interface import CameraInterface  
from main import *

#Set up option parsing to get connection string
import argparse
import numpy as np
import json
import pandas as pd
import cv2


def edit_json(newFlight):
    
    with open('/home/pi/Desktop/HF-LOCUST-WASP/results.json', 'r+') as f:
        data = []
        try:
            data = json.load(f)
        except:
            print("Empty json")
            
        data.append(newFlight)
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        f.close()

    print("done")


def write_json(timestamp, num, percentage, data_drone, image_settings, path):
    coordinates = (data_drone[0], data_drone[1])
    results.append(
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
        "results": results
    }

    return flight

def create_directory():  # tested and working
  
    path = '/home/pi/Desktop/HF-LOCUST-WASP/public/results/photos'
    # we need to convert numbers to string to be able to create the new path
    year = str(pd.datetime.now().year)
    month = str(pd.datetime.now().month)
    day = str(pd.datetime.now().day)
    hour = str(pd.datetime.now().hour)
    minute = str(pd.datetime.now().minute)
    global timestamp

    timestamp = year + "_" + month + "_" + day + "-" + hour + "_" + minute
    newpath = path + "/" + timestamp  # we create the string for the new directory
    
    os.mkdir(newpath)        # creates a directory
    normal_images = newpath + '/' + 'raw_images'
    ndvi_images = newpath + '/' + 'ndvi_images'
    os.mkdir(normal_images)
    os.mkdir(ndvi_images)
    
    return newpath

def contrast_stretch(im):
    """
    Performs a simple contrast stretch of the given image, from 5-95%.
    """
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def main_loop(vehicle, num, newpath, camera_interface, autopilot_interface):
    
    img = camera_interface.capture_frame()

   # Once we have a gray colorspace mask, we want to add the orginal image to it
    b = np.array(img[:, :, 0]).astype(float) + 0.00000000001
    g = np.array(img[:, :, 1]).astype(float)
    r = np.array(img[:, :, 2]).astype(float) + 0.00000000001

    nir = r
    red = b

    np.seterr(divide='ignore', invalid='ignore')

    ndvi = ((nir - red) / (nir + red)).astype(float)

    #Once we have the ndvi matrix, we want to know how many values are following the ndvi condition
    values_ndvi = np.count_nonzero(ndvi > 0.14)
    ndvi[ndvi<0.14] = 0
    
    # we multiply the number of rows by the number of columns to obtain the total number of values
    total_values = ndvi.shape[0] * ndvi.shape[1]

    percent = round(((values_ndvi / total_values) * 100), 2)

    if percent >= -10:
        
        name = newpath + '/' + 'raw_images'+'/' + str(num) + '.jpeg'
        name_ndvi = newpath + '/' + 'ndvi_images' + '/' + str(num) + '.jpeg'
    
        # name = path + '/' + 'ndvi_results' + '/' + 'image' + 'ndvi' + str(percent) + '.jpeg'

        cv2.imwrite(name, img)
        
        ndvi_new = contrast_stretch(ndvi).astype(np.uint8)
        cv2.imwrite(name_ndvi, ndvi_new)

        data_drone = autopilot_interface.set_data_drone()

        image_settings = camera_interface.camera_settings()
        
        path_json = '/results/photos/' + str(timestamp) + '/' + 'raw_images'+'/' + str(num) + '.jpeg'
        flight_info = write_json(timestamp, num, percent, data_drone, image_settings, path_json)

        print('@@@ image processed @@@')
        return flight_info
    
    else:

        name = newpath + '/' + 'raw_images' + '/' + str(num) + '.jpeg'
        name_ndvi = newpath + '/' + 'ndvi_images' + '/' + str(num) + '.jpeg'

        # name = path + '/' + 'ndvi_results' + '/' + 'image' + 'ndvi' + str(percent) + '.jpeg'

        cv2.imwrite(name, img)

        ndvi_new = contrast_stretch(ndvi).astype(np.uint8)

        cv2.imwrite(name_ndvi, ndvi_new)
        return None

def main(vehicle):

    global num
    num = 1
    camera_interface = CameraInterface()
    autopilot_interface = AutopilotInterface(vehicle)
    newpath = create_directory()
    
    while vehicle.armed is True:
        
        altitude = autopilot_interface.get_altitude()
        
        if altitude >= -50:
            
            flight_data = main_loop(vehicle, num, newpath, camera_interface, autopilot_interface)
            camera_interface.test_settings(num)
            num += 1
    
    if (flight_data != None):
        try:
            edit_json(flight_data)
        except:
            print("No flight")
    
    else:
        print('Flight data is empty')
                    


def armDrone():

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready

    print("Arming motors")
    # Copter should arm in GUIDED mode
    # vehicle.mode = VehicleMode("AUTO")

    vehicle.armed = True
    vehicle.mode = VehicleMode("AUTO")

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

    print("Done!")
    


connection_string = "/dev/ttyS0"
sitl = None

#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle. 
#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
#print("\nConnecting to vehicle on: %s" % connection_string)

vehicle = connect(connection_string, baud=921600, wait_ready=True)
  
results = []
  
# Get some vehicle attributes (state)
cmds = vehicle.commands
cmds.download()

armDrone()
main(vehicle)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator




