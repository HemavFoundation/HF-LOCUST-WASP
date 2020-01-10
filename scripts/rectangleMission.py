from __future__ import print_function
from math import asin,cos,pi,sin

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil

rEarth = 6371.01 # Earth's average radius in km
epsilon = 0.000001 # threshold for floating-point equality


def deg2rad(angle):
    return angle*pi/180

def download_mission():
    """
    Downloads the current mission and returns it in a list.
    It is used in save_mission() to get the file information to save.
    """
    missionlist=[]
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    for cmd in cmds:
        missionlist.append(cmd)
    return missionlist


def save_mission(aFileName):
    """
    Save a mission in the Waypoint file format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).
    """
    missionlist = download_mission()
    output='QGC WPL 110\n'
    for cmd in missionlist:
        commandline="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (cmd.seq,cmd.current,cmd.frame,cmd.command,cmd.param1,cmd.param2,cmd.param3,cmd.param4,cmd.x,cmd.y,cmd.z,cmd.autocontinue)
        output+=commandline
    with open(aFileName, 'w') as file_:
        file_.write(output)


def rad2deg(angle):
    return angle*180/pi


def pointRadialDistance(lat1, lon1, bearing, distance):
    """
    Return final coordinates (lat2,lon2) [in degrees] given initial coordinates
    (lat1,lon1) [in degrees] and a bearing [in degrees] and distance [in km]
    """
    rlat1 = deg2rad(lat1)
    rlon1 = deg2rad(lon1)
    degreeBearing = ((360-bearing)%360)
    rbearing = deg2rad(degreeBearing)
    rdistance = (distance)  / rEarth # normalize linear distance to radian angle

    rlat = asin(sin(rlat1) * cos(rdistance) + cos(rlat1) * sin(rdistance) * cos(rbearing) )

    if cos(rlat) == 0 or abs(cos(rlat)) < epsilon: # Endpoint a pole
        rlon=rlon1
    else:
        rlon = ( (rlon1 - asin( sin(rbearing)* sin(rdistance) / cos(rlat) ) + pi ) % (2*pi) ) - pi

    lat = rad2deg(rlat)
    lon = rad2deg(rlon)
    return LocationGlobal(lat, lon,0)

   
def flight(lat1, lon1, bearing, distance, spaceDistance, widthRectangle):

    number = 10
    finalPoint = pointRadialDistance(lat1, lon1, bearing, (distance + 0.5))

    # we're going to calculate the mission, we need some space for the takeoff of the drone and this space will be 500 meters and the width of the rectangle in this case will be 500m
    fase = rad2deg(math.atan((widthRectangle/2)/spaceDistance))
    print(fase)
    h = (widthRectangle/2)/math.sin(deg2rad(fase))
    print(h)
    firstLocation = pointRadialDistance(lat1,lon1,(bearing + fase),h)

    #takeoff
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, number))
    number += 1
    
    #first point
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstLocation.lat, firstLocation.lon, number))
    number += 1


    print(finalPoint.lat, finalPoint.lon)
    print(firstLocation.lat, firstLocation.lon)

    #second point
    locationLoop = pointRadialDistance(firstLocation.lat, firstLocation.lon, bearing - 90, widthRectangle)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, number))
    number += 1

    division = (distance / 0.250) / 2 #
    print(division)
    print(locationLoop.lat, locationLoop.lon)

    for x in range(int(division)):
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, bearing, distance/20)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, number))
        number += 1
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, bearing + 90, widthRectangle)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, number))
        number += 1
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, bearing, distance/20)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, number))
        number += 1
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, bearing - 90, widthRectangle)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, number))
        number += 1
        print (locationLoop.lat,locationLoop.lon)
    
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, lat1, lon1, number))
    number += 1
    
    


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
vehicle = connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
cmds = vehicle.commands

cmds.download()
cmds.wait_ready()

cmds.clear()
    
 
flight(41.2755578,1.987257,269,5,0.5,0.5)

print(" Upload new commands to vehicle")
cmds.upload()
save_mission('./hola')

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()


