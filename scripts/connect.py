#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
#from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
from dronekit import *
import time

connection_string = "/dev/ttyS0"
sitl = None

#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

vehicle = None

while vehicle is None:
    vehicle = connect(connection_string, baud=921600, wait_ready=False)

# Get some vehicle attributes (state)
cmds = vehicle.commands


print(vehicle.heading)
print(vehicle.location.global_frame.lat)
print(vehicle.location.global_frame.lon)
print(vehicle.location.global_frame.alt)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator

