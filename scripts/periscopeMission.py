from __future__ import print_function
from math import asin,cos,pi,sin

#from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
from dronekit import *
import time
import math
from pymavlink import mavutil
from commonFunctions import *
from config import *
from flights import *
import sys

if connectionString != "local":
    distance = float(sys.argv[1]) / 1000
    widthRectangle = float(sys.argv[3]) / 1000
    spaceDistance = float(sys.argv[2]) / 1000
    spaceBtwLines = float(sys.argv[4]) / 1000
    height = int(sys.argv[5])

    connection_string = "/dev/ttyS0"
    latFlight = int(sys.argv[6])
    lonFlight = int(sys.argv[7])
    headingFlight = int(sys.argv[8])

else:
    connection_string = None
    latFlight = -35.363261
    lonFlight = 149.165229
    headingFlight = 353
    height = 120


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

latWind = vehicle.location.global_frame.lat
lonWind = vehicle.location.global_frame.lon
headingWind = vehicle.heading

cmds = periscopeMission(latWind, lonWind, headingWind, height, latFlight, lonFlight, cmds)

print(" Upload new commands to vehicle")

typeOfMission = "straight"


if connectionString == "local":
    save_mission('./hola.waypoints', cmds)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()



