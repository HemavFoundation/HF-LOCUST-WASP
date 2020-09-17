from __future__ import print_function

import multiprocessing
import threading
from image_processing.autopilot_interface import AutopilotInterface
from dronekit import *
from commonFunctions import *
from config import *
import time




vehicle = connect("/dev/ttyS0", baud=921600, wait_ready=False)
  
print('#### connected ####')

def lat():
    autopilot_interface = AutopilotInterface(vehicle)
    print(autopilot_interface.get_latitude())


def lon():
    autopilot_interface = AutopilotInterface(vehicle)
    print(autopilot_interface.get_longitude())   


p1 = multiprocessing.Process(target=lat)
p2 = multiprocessing.Process(target=lon)

p1.start()
p2.start()

p1.join()
p2.join()