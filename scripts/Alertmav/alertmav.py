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


if __name__ == "__main__":

    while (1):
            
        previous = time.perf_counter()
        satellite_timer = 0


        while vehicle.armed is True:        

            current = time.perf_counter()
            satellite_timer += current - previous
            time.sleep(1)
            print('Satellite timer:', satellite_timer)
            previous = current

            if satellite_timer > 30:  # we want to send location every 60 seconds
                
                sendLocation(autopilot_interface.get_latitude(), autopilot_interface.get_longitude(), autopilot_interface.get_altitude(), autopilot_interface.get_heading())
                satellite_timer = 0
        
        if( vehicle.armed == False):
            time.sleep(1)
            print('El drone no está armado')




