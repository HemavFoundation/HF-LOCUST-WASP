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


distance = float(sys.argv[1]) / 1000
widthRectangle = float(sys.argv[3]) / 1000
spaceDistance = float(sys.argv[2]) / 1000
spaceBtwLines = float(sys.argv[4]) / 1000
height = int(sys.argv[5])


# distance = float(1000) / 1000
# widthRectangle = float(100) / 1000
# spaceDistance = float(200) / 1000
# spaceBtwLines = float(100) / 1000
# height = int(120)


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
global cmds

cmds = vehicle.commands

latWind = vehicle.location.global_frame.lat
lonWind = vehicle.location.global_frame.lon
headingWind = vehicle.heading

#rectangleMission can change between reversed or normal depending how you want to make the mission

#cmds = rectangleMission_reversed(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight, cmds)

if connectionString != "local":
    cmds = rectangleMission_normal(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight, cmds)
    #cmds = rectangleMission_reversed(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight, cmds)

else:
    cmds = rectangleMission_normal(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, float(34.5), float(45.3), int(234), cmds)
    #cmds = rectangleMission_reversed(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight, cmds)


#cmds= rectangleMission_normal(float(34.5),float(23.3),int(342),)
#cmds = rectangleMission_normal(latWind, lonWind, headingWind,int(120),int(120),int(500),int(120),int(120),latFlight,lonFlight,headingWind,cmds)

print(" Upload new commands to vehicle")

#save_mission('./hola.waypoints', cmds)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()



