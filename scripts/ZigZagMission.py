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
width = float(sys.argv[2]) / 1000
periodDistance = float(sys.argv[3]) / 1000
height = int(sys.argv[4])

if connectionString != "local":
    connection_string = "/dev/ttyS0"
    latFlight = int(sys.argv[5])
    lonFlight = int(sys.argv[6])
    headingFlight = int(sys.argv[7])

else:
    connection_string = None
    latFlight = -35.363261
    lonFlight = 149.165229
    headingFlight = 90

#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

global cmds
vehicle = connect(connection_string, baud=921600, wait_ready=True) #objeto con el cual vamos a interactuar con la controladora del dron y nos va a dar datos
cmds = vehicle.commands # vehicle commands es donde vamos a ir registrando todos los puntos de control de vuelo (waypoints) donde finalmente se los pasaremos de nuevo a la controladora y esta sabrá que pasos ha de realizar para volar

latWind = vehicle.location.global_frame.lat #recogemos la latitud actual del drone
lonWind = vehicle.location.global_frame.lon #recogemos la longitud actual del drone
headingWind = vehicle.heading #recogemos el heading actual del drone

if inverse == False:
    cmds = ZigZagMission(latWind,lonWind,headingWind,distance,periodDistance,width,height,latFlight,lonFlight,headingFlight,cmds)
else:
    cmds = ZigZagMissionInversed(latWind, lonWind, headingWind, distance, periodDistance, width, height, latFlight, lonFlight, headingFlight, cmds)


print("New commands uploaded")

typeOfMission = "zigzag"


if connectionString == "local":
    save_mission('./hola.waypoints', cmds)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()