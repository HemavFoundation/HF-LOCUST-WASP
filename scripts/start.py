from __future__ import print_function
#from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
from dronekit import *
import time
import os
from autopilot_interface import AutopilotInterface
from camera_interface import CameraInterface  
from main import *
#from image_processing.interfaces.autopilot_interface import AutopilotInterface
#from image_processing.interfaces.interfaces.camera_interface import CameraInterface
#Set up option parsing to get connection string
import argparse
import numpy as np
import json
import pandas as pd
import cv2


def edit_json(newFlight, output_file):

    with output_file as f:
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
    results = []

    coordinates = (data_drone[0], data_drone[1])
    results.append(
        {
                "image_id": num,
                "percentage": percentage,
                "coordinates": coordinates,
                "image path": path,
                "camera settings": image_settings,
            }
    )

    flight = {
        "id": timestamp,
        "results": results
    }

    return flight

def create_directory():  # tested and working

    # path = os.getcwd()  # this returns actual directory as a string (should be modify to a raspberry directory)
    
    path = '/home/pi/Desktop/locust_vegetation_finder_images'
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

def main_loop(num, newpath, camera_interface, autopilot_interface):
    
    print('@@@@ entered main loop @@@')
    
    img = camera_interface.capture_frame()
    print('@@@@ obtained image from camera @@@')

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

    # we multiply the number of rows by the number of columns to obtain the total number of values
    total_values = ndvi.shape[0] * ndvi.shape[1]

    percent = round(((values_ndvi / total_values) * 100), 2)

    if percent >= 10:

        path = os.getcwd()
        
        name = newpath + '/' + 'raw_images'+'/' + str(num) + '.jpeg'
        name_ndvi = newpath + '/' + 'ndvi_images'+'/'+ str(num) + '.jpeg'

        # name = path + '/' + 'ndvi_results' + '/' + 'image' + 'ndvi' + str(percent) + '.jpeg'

        cv2.imwrite(name, img)
        
        ndvi_new = contrast_stretch(ndvi).astype(np.uint8)
        cv2.imwrite(name_ndvi, ndvi_new)

        data_drone = autopilot_interface.set_data_drone()

        image_settings = camera_interface.camera_settings()

        flight = write_json(timestamp, num, percent, data_drone, image_settings, path)

        print('@@@ image processed @@@')

    else:
        path = os.getcwd()

        name = newpath + '/' + 'raw_images' + '/' + str(num) + '.jpeg'
        name_ndvi = newpath + '/' + 'ndvi_images' + '/' + str(num) + '.jpeg'

        # name = path + '/' + 'ndvi_results' + '/' + 'image' + 'ndvi' + str(percent) + '.jpeg'

        cv2.imwrite(name, img)

        ndvi_new = contrast_stretch(ndvi).astype(np.uint8)

        image_settings = camera_interface.camera_settings()
        data_drone = autopilot_interface.set_data_drone()
        cv2.putText(ndvi_new, (image_settings, data_drone), (10, 10), FONT_HERSHEY_SIMPLEX, (255, 255, 255))
        cv2.imwrite(name_ndvi, ndvi_new)


    return flight

def main(vehicle):

    output_file = open('/home/pi/Desktop/HF-LOCUST-WASP/results.json', 'r+')  # condition must be 'a' to do not rewrite the json file on each flight

    global num
    num = 1
    camera_interface = CameraInterface()
    autopilot_interface = AutopilotInterface(vehicle)
    newpath = create_directory()
    
    while vehicle.armed is True:
        
        altitude = autopilot_interface.get_altitude()
        print('@@@@@@altitude @@@@', altitude)
        
        if altitude >= 50:
            
            flight = main_loop(num, newpath, camera_interface, autopilot_interface)
            camera_interface.test_settings(num)
            num += 1

    try:
        edit_json(flight, output_file)
    except:
        print("No flight")


#if __name__ == '__main__':
    #main()


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
    
  
# Get some vehicle attributes (state)
cmds = vehicle.commands
cmds.download()
#cmds.wait_ready()
armDrone()
main(vehicle)

#timeout test
time.sleep(86000)


# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator




