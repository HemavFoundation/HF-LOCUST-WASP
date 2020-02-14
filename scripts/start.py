from __future__ import print_function
from dronekit import *
import time
import os

from scripts.image_processing.autopilot_interface import AutopilotInterface
from scripts.image_processing.camera_interface import CameraInterface
from scripts.image_processing import main
#Set up option parsing to get connection string
import argparse
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

armDrone()
global num
results = []
num = 1
camera_interface = CameraInterface()
autopilot_interface = AutopilotInterface(vehicle)
newpath = main.create_directory()
flight_data = None

while vehicle.armed is True:

    altitude = autopilot_interface.get_altitude()

    if altitude >= 50:
        flight_data = main.main_loop(vehicle, num, newpath, camera_interface, autopilot_interface)
        camera_interface.test_settings(num)
        num += 1

if flight_data is not None:
    try:
        main.edit_json(flight_data)
    except:
        print("No flight")
else:
    print('Flight data is empty')

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()





