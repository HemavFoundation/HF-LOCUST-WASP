from __future__ import print_function
from math import asin, cos, pi, sin

#from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
from dronekit import *
import time
import math
from pymavlink import mavutil
from commonFunctions import *
from config import *
from flights import *
import sys


distance = int(sys.argv[1]) / 1000
height = int(sys.argv[2]) / 1000

sitl = None

if connectionString != "local":
    connection_string = "/dev/ttyS0"

    latFlight = float(sys.argv[3])
    lonFlight = float(sys.argv[4])
    headingFlight = int(sys.argv[5])

else:
    connection_string = None
    latFlight = -35.363261
    lonFlight = 149.165229
    headingFlight = 353


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Get some vehicle attributes (state)
global cmds

# objeto con el cual vamos a interactuar con la controladora del dron y nos va a dar datos
vehicle = connect(connection_string, baud=921600, wait_ready=True)


# vehicle commands es donde vamos a ir registrando todos los puntos de control de vuelo (waypoints) donde finalmente se los pasaremos de nuevo a la controladora y esta sabrá que pasos ha de realizar para volar
cmds = vehicle.commands

# recogemos la latitud actual del drone
latWind = vehicle.location.global_frame.lat
# recogemos la longitud actual del drone
lonWind = vehicle.location.global_frame.lon
headingWind = vehicle.heading  # recogemos el heading actual del drone


cmds_final = straightMission(latWind, lonWind, headingWind, distance, height, latFlight,
                             lonFlight, headingFlight, cmds)  # lineal mission devuelve un objeto cmds relleno

print(" Upload new commands to vehicle")

typeOfMission = "straight"

if connectionString == "local":
    save_mission('./hola.waypoints', cmds_final)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()
