#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
vehicle_state.py: 

Demonstrates how to get and set vehicle state and parameter information, 
and how to observe vehicle attribute (state) changes.

Full documentation is provided at http://python.dronekit.io/examples/vehicle_state.html
"""
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


# Connect to the Vehicle. 
#   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
#print("\nConnecting to vehicle on: %s" % connection_string)

vehicle = None

while vehicle is None:
    vehicle = connect(connection_string, baud=921600, wait_ready=True)



# Get some vehicle attributes (state)
cmds = vehicle.commands
#cmds.download()
#cmds.wait_ready()

# heading = vehicle.heading

# globalLocation = "%s" % vehicle.location.global_frame
# test = globalLocation.split("=")
# split1 = "%s" % test[1]
# split2 = "%s" % test[2]

# alt = "%s" % test[3]
# lat = "%s" % split1.split(",")[0]
# lon = "%s" % split2.split(",")[0]


print(vehicle.heading)
print(vehicle.location.global_frame.lat)
print(vehicle.location.global_frame.lon)
print(vehicle.location.global_frame.alt)
# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()

