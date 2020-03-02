from __future__ import print_function
from dronekit import *
import time
import os
from commonFunctions import *
from config import *
from image_processing.autopilot_interface import AutopilotInterface
from image_processing.camera_interface import CameraInterface
from image_processing import main
import geopy.distance
from time import perf_counter
#Set up option parsing to get connection string
import argparse
import numpy as np
import json
import pandas as pd
import cv2


# Function to implement an RTL in case of low battery level to be able to come back home
def battery_check(home_coordinates):

    # energy parameters
    battery_capacity = 5700 # in mAh
    percentage = vehicle.battery.level
    battery_low = 21.3   # 3,55V per each battery cell (6 in total): 3.55*6
    current_consumption = vehicle.battery.current
    actual_voltage = vehicle.battery.voltage

    # kinematic parameters
    speed = vehicle.groundspeed
    actual_coordinates = (autopilot_interface.get_latitude, autopilot_interface.get_longitude)

    remaining_capacity = battery_capacity * percentage
    distance = geopy.distance.vincenty(actual_coordinates, home_coordinates).meters

    time_capacity = (remaining_capacity / current_consumption) * 3.6 # estimated capacity remaining in seconds
    time_to_home = distance * speed  # estimated time in seconds to reach home

    return time_capacity, time_to_home


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

if connectionString != "local":
    connection_string = "/dev/ttyS0"
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
  

  
# Get some vehicle attributes (state)
cmds = vehicle.commands
cmds.download()

camera_interface = CameraInterface()
autopilot_interface = AutopilotInterface(vehicle)

# we get the home coordinates to introduce them in the intelligent RTL function
home_coordinates = (autopilot_interface.get_latitude, autopilot_interface.get_longitude)

armDrone()
global num


results = []
num = 1
elapsed_time = 0

newpath = main.create_directory()
flight_data = None


if connectionString != "local":
    altitudeCondition = 50 
else:
    altitudeCondition = -50


while vehicle.armed is True:

    time_capacity, time_to_home = battery_check(home_coordinates)

    if time_capacity < time_to_home:
        timer_beginning = perf_counter()
    else:
        elapsed_time = None
        timer_beginning = 0

    altitude = autopilot_interface.get_altitude()
    
    if altitude >= altitudeCondition:
        flight_data = main.main_loop(vehicle, num, newpath, camera_interface, autopilot_interface)
        camera_interface.test_settings(num)
        num += 1

    if time_capacity < time_to_home:
        timer_end = perf_counter()
        elapsed_time = elapsed_time + (timer_end - timer_beginning)
    else:
        elapsed_time = None

    if elapsed_time > 30:
        vehicle.mode = VehicleMode("RTL")

if flight_data is not None:
    try:
        main.edit_json(flight_data)
    except:
        print("No flight")
else:
    try:
        results[0] = 'No vegetation found'
        main.edit_json(flight_data)
        print("No vegetation found")
        
    except:
        
        print('Flight data is empty')
    
    

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()





