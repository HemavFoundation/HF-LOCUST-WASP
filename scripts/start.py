from __future__ import print_function
from dronekit import *
import time
import os
from commonFunctions import *
from config import *
from image_processing.autopilot_interface import AutopilotInterface
from image_processing.camera_interface import CameraInterface
from image_processing.visual_camera_interface import VisualCameraInterface
from image_processing.data_management import DataManagement
from image_processing import main
import geopy.distance
import numpy as np
import json
import pandas as pd
import cv2
import multiprocessing
import serial
from adafruit_rockblock import RockBlock
from RockClient import *

if connectionString != "local":
    connection_string = "/dev/serial0"
else:
    connection_string = None
    
sitl = None

if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


vehicle = connect(connection_string, baud=921600, wait_ready=True)
  
print('#### connected ####')
  
# Get some vehicle attributes (state)
cmds = vehicle.commands
cmds.download()

rc = RockClient()

def sendLocation():

    autopilot_interface = AutopilotInterface(vehicle)
    
    latitude = autopilot_interface.get_latitude()
    longitude = autopilot_interface.get_longitude()
    altitude = autopilot_interface.get_altitude()
    heading = autopilot_interface.get_heading()
    
    rc.send_location(latitude,longitude,altitude,heading)


def cameras():
    
    path_mono, path_visual, raw_images, timestamp = main.create_directory()

    camera_interface = CameraInterface()
    autopilot_interface = AutopilotInterface(vehicle)
    visualcamera_interface = VisualCameraInterface(timestamp)
    data_interface = DataManagement()

    # we get the home coordinates to introduce them in the intelligent RTL function
    home_coordinates = (autopilot_interface.get_latitude, autopilot_interface.get_longitude)

    global num
    global num_visual

    num = 1
    num_visual = 1


    # Json structures containing all the data
    flight_data = None

    if  connectionString != "local":
        altitudeCondition = -50
    else:
        altitudeCondition = -50

    # We initialize time variables for the visual camera 
    previous = time.perf_counter()
    delta_time = 0

    print('type of mission:', typeOfMission)

    if typeOfMission in ["straight", "zigzag", "rectangle"]:
        
        while vehicle.armed is True:
            print(vehicle.armed)
            altitude = autopilot_interface.get_altitude()
            current = time.perf_counter()
            delta_time += current - previous
            print(delta_time)
            previous = current
            

            if altitude >= altitudeCondition:
                flight_data = main.main_loop_mono(num, path_mono, raw_images, camera_interface, autopilot_interface, data_interface)
                camera_interface.test_settings(num)
                num += 1

            if delta_time > 5:  # we want to take images every 30 seconds
                flight_data = main.main_loop_visual(num_visual, path_visual, visualcamera_interface, autopilot_interface, data_interface)
                num_visual += 1                
                delta_time = 0

        if flight_data is not None:
            try:
                data_interface.edit_json(flight_data)
                print('json written')
            except:
                print('could not write json')
        else: 
            print('Empty json')

    if typeOfMission is "periscope":
        print('periscope mission')
        while vehicle.armed is True:

            altitude = autopilot_interface.get_altitude()

            if altitude >= altitudeCondition:  # on the periscope mission we just one to make as much photos as possible with the visual camera
                flight_data = main.main_loop_visual(num_visual, path_visual, visualcamera_interface, autopilot_interface, data_interface)
                num_visual += 1

        if flight_data is not None:
            try:
                data_interface.edit_json(flight_data)
                print('json written')
            except:
                print('could not write json')
        else:
            print('flight data is empty')



p1 = multiprocessing.Process(target=cameras)
p2 = multiprocessing.Process(target=sendLocation)

p1.start()
p2.start()

a = 1

while a is 1:
    if(vehicle.armed is False):
        p1.kill()
        p2.kill()
        a = 0
        break
    
# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()










