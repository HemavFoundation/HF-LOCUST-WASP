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
from time import time
from time import sleep
import numpy as np
import json
import pandas as pd
import cv2


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
        sleep(1)

    print("Done!")

if connectionString != "local":
    connection_string = "/dev/serial0"
else:
    connection_string = None
    
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
  
print('#### connected ####')
  
# Get some vehicle attributes (state)
cmds = vehicle.commands
cmds.download()

camera_interface = CameraInterface()
autopilot_interface = AutopilotInterface(vehicle)
visualcamera_interface = VisualCameraInterface()
data_interface = DataManagement()

# we get the home coordinates to introduce them in the intelligent RTL function
home_coordinates = (autopilot_interface.get_latitude, autopilot_interface.get_longitude)

armDrone()
global num
global num_visual

num = 1
num_visual = 1

newpath_mono, newpath_visual = main.create_directory()

# Json structures containing all the data
flight_data = None

if connectionString != "local":
    altitudeCondition = 50
else:
    altitudeCondition = -50

# We initialize time variables for the visual camera 
previous = time()
delta_time = 0

if typeOfMission is "straight" or "zigzag" or "rectangle":
    while vehicle.armed is True:

        altitude = autopilot_interface.get_altitude()
        current = time()
        delta_time += current - previous
        previous = current

        if altitude >= altitudeCondition:
            flight_data = main.main_loop_mono(num, newpath_mono, camera_interface, autopilot_interface, data_interface)
            camera_interface.test_settings(num)
            num += 1

        if delta_time > 30:  # we want to take images every 30 seconds
            flight_data = main.main_loop_visual(num_visual, newpath_visual, visualcamera_interface, autopilot_interface, data_interface)
            num_visual += 1

    if flight_data is not None:
        try:
            data_interface.edit_json(flight_data)
            print('json written')
        except:
            print('could not write json')
    else: 
        print('Empty json')

if typeOfMission is "periscope":
    while vehicle.armed is True:

        altitude = autopilot_interface.get_altitude()

        if altitude >= altitudeCondition:  # on the periscope mission we just one to make as much photos as possible with the visual camera
            flight_data = main.main_loop_visual(num_visual, newpath_visual, visualcamera_interface, autopilot_interface, data_interface)
            num_visual += 1

    if flight_data is not None:
        try:
            data_interface.edit_json(flight_data)
            print('json written')
        except:
            print('could not write json')
    else:
        print('could not save the json properly')
        
# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()





