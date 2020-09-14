from __future__ import print_function
from dronekit import *
import time
import os
from commonFunctions import *
from config import *
from time import time
from time import sleep
import numpy as np
import json
import pandas as pd


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


# Get some vehicle attributes (state)
global cmds
cmds = vehicle.commands

armDrone()  


# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()
