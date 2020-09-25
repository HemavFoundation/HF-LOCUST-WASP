import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
from adafruit_rockblock import RockBlock
from autopilot_interface import AutopilotInterface
from RockClient import *
from dronekit import *
from config import *
import time


if connectionString != "local":
    #print('connection string imported:', flight_controller['port'])
    connection_string = flight_controller['port']
else:
    connection_string = None
    
sitl = None


if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

baudrate = flight_controller['baudrate']
vehicle = connect(connection_string, baud=baudrate, wait_ready=True)

cmds = vehicle.commands
cmds.download()

rc = RockClient()
autopilot_interface = AutopilotInterface(vehicle)


def sendLocation(lat,lon,alt, heading):
    
    rc.send_location(lat,lon,alt, heading)

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
        time.sleep(1)

    print("Done!")

if __name__ == "__main__":
    
    armDrone()

    while (1):           
        
        
        previous = time.perf_counter()
        satellite_timer = 0
        altitude = autopilot_interface.get_altitude()


        while altitude > 25:        

            current = time.perf_counter()
            satellite_timer += current - previous
            time.sleep(1)
            print('Satellite timer:', satellite_timer)
            previous = current

            if satellite_timer > 30:  # we want to send location every 60 seconds
                sendLocation(autopilot_interface.get_latitude(), autopilot_interface.get_longitude(), autopilot_interface.get_altitude(), autopilot_interface.get_heading())
                satellite_timer = 0
                previous = time.perf_counter()
                
        
        if( altitude < 25):
            time.sleep(1)
            print('No se cumple la condicion de altitud. Altitud actual: ', altitude)




