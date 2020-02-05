from __future__ import print_function
from math import asin,cos,pi,sin

#from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
from dronekit import *
import time
import math
from pymavlink import mavutil
import sys

#sys.argv[1]


distance = int(sys.argv[1]) / 1000
widthRectangle = int(sys.argv[2]) / 1000
spaceDistance = int(sys.argv[3]) / 1000
spaceBtwLines = int(sys.argv[4]) / 1000
height = int(sys.argv[5])
latFlight = float(sys.argv[6])
lonFlight = float(sys.argv[7])
headingFlight = int(sys.argv[8])

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

   
def flight(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight):

    finalPoint = pointRadialDistance(latWind, lonWind, headingWind, (distance + spaceDistance))

    # we're going to calculate the mission, we need some space for the takeoff of the drone and this space will be 500 meters and the width of the rectangle in this case will be 500m
    fase = rad2deg(math.atan((widthRectangle/2)/spaceDistance))
    print(fase)
    h = (widthRectangle/2)/math.sin(deg2rad(fase))
    print(h)
    firstLocation = pointRadialDistance(latFlight,lonFlight,(headingFlight + fase),h)
    firstLandingWaypoint = pointRadialDistance(latWind, lonWind, (headingWind + 180), 0.1)
    secondLandingWaypoint = pointRadialDistance(firstLandingWaypoint.lat, firstLandingWaypoint.lon, (headingWind + 180), 0.1)


    #takeoff
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 0, 1, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 0, 1, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 10, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, 0, 0, 0, 17, 0, 0, 0, 0, height))
    #first point
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstLocation.lat, firstLocation.lon, height))


    print(finalPoint.lat, finalPoint.lon)
    print(firstLocation.lat, firstLocation.lon)

    #second point
    locationLoop = pointRadialDistance(firstLocation.lat, firstLocation.lon, headingWind - 90, widthRectangle)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))

    division = (distance / spaceBtwLines) / 2 #
    print(division)
    print(locationLoop.lat, locationLoop.lon)

    for x in range(int(division)):
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingWind, spaceBtwLines)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingWind + 90, widthRectangle)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingWind, spaceBtwLines)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingWind - 90, widthRectangle)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_LAND_START, 0, 0, 0, 0, 0, 0, latWind, lonWind, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latWind, lonWind, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 0, 0, 0, 0, 0, latWind, lonWind, 30))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, secondLandingWaypoint.lat, secondLandingWaypoint.lon, 30))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstLandingWaypoint.lat, firstLandingWaypoint.lon, 30))

    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, latWind, lonWind, 30))
    
    cmds.upload()


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

vehicle = connect(connection_string, baud=921600, wait_ready=True)


# Get some vehicle attributes (state)
global cmds

cmds = vehicle.commands

latWind = vehicle.location.global_frame.lat
lonWind = vehicle.location.global_frame.lon
headingWind = vehicle.heading


flight(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight)

print(" Upload new commands to vehicle")

save_mission('./hola.waypoints')

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
if sitl is not None:
    sitl.stop()



