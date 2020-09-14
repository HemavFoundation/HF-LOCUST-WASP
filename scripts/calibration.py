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
msg = vehicle.message_factory.command_long_encode(
            0, 0,  # target_system, target_component
            mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION,  # command
            0,  # confirmation
            1,  # param 1, 1: gyro calibration, 3: gyro temperature calibration
            0,  # param 2, 1: magnetometer calibration
            0,  # param 3, 1: ground pressure calibration
            0,  # param 4, 1: radio RC calibration, 2: RC trim calibration
            0,  # param 5, 1: accelerometer calibration, 2: board level calibration, 3: accelerometer temperature calibration, 4: simple accelerometer calibration
            2,  # param 6, 2: airspeed calibration
            0)  # param 7, 1: ESC calibration, 3: barometer temperature calibration
# send command to vehicle
vehicle.send_mavlink(msg)
NEW
 print("llego hasta aquí")


# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()
