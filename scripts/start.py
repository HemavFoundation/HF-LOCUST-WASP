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
from flights import *
#Set up option parsing to get connection string
import argparse
import numpy as np
import json
import pandas as pd
import cv2


# Function to implement an RTL in case of low battery level to be able to come back home
def battery_check(home_coordinates, timer_start, elapsed_time):

    # energy parameters
    battery_capacity = 5700 # in mAh
    percentage = vehicle.battery.level
    battery_high = 26.2   # 4.2 V per each cell (dji maxim is 26.2)
    battery_low = 21.3   # 3,55V per each battery cell (6 in total): 3.55*6
    current_consumption = vehicle.battery.current       # current consumption in amperes
    actual_voltage = vehicle.battery.voltage    # voltage in volts


    # kinematic parameters
    speed = vehicle.groundspeed    # groundspeed in m/s
    actual_coordinates = (autopilot_interface.get_latitude, autopilot_interface.get_longitude)

    remaining_capacity = battery_capacity * percentage
    distance = geopy.distance.vincenty(actual_coordinates, home_coordinates).meters

    time_capacity = (remaining_capacity / current_consumption) * 3.6 # estimated capacity remaining in seconds
    time_to_home = distance * speed  # estimated time in seconds to reach home

    if time_capacity < time_to_home and timer_start is None:
        timer_start = time.time()

    if time_capacity < time_to_home and timer_start is not None:
        timer_actual = time.time()
        elapsed_time = timer_actual - timer_start

    if time_capacity > time_to_home:
        timer_start = None
        elapsed_time = 0

    if elapsed_time > 30:
        battery_failsafe = True
    else:
        battery_failsafe = False

    return battery_failsafe, timer_start, elapsed_time


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

# we need to initiate the faislafe parameters:
elapsed_time = 0
timer_start = None
battery_failsafe = False

results = []
num = 1

newpath = main.create_directory()
flight_data = None


if connectionString != "local":
    altitudeCondition = 50 
else:
    altitudeCondition = -50


while vehicle.armed is True:

    altitude = autopilot_interface.get_altitude()
    
    if altitude >= altitudeCondition:
        flight_data = main.main_loop(vehicle, num, newpath, camera_interface, autopilot_interface)
        camera_interface.test_settings(num)
        num += 1

    battery_failsafe, timer_start, elapsed_time = battery_check(home_coordinates, timer_start, elapsed_time)

    if battery_failsafe is True:
        landing(latWind, lonWind, headingWind, cmds)

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





