#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from dronekit import *
from commonFunctions import *
from config import *
import time

if(connectionString != "local"):
    connection_string = "/dev/ttyS0"
else:
    connection_string = None
    
sitl = None

# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

vehicle = None

while vehicle is None:
    vehicle = connect(connection_string, baud=921600, wait_ready=True)

# Get some vehicle attributes (state)
vehicle.send_calibrate_barometer()

print("llego hasta aquí")


# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()
