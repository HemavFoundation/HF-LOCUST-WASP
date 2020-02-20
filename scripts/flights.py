from commonFunctions import *
from config import *
from math import asin,cos,pi,sin

def landing(latWind, lonWind, headingWind, cmds):
    firstLandingWaypoint = pointRadialDistance(latWind, lonWind, (headingWind + 180), 0.1)
    secondLandingWaypoint = pointRadialDistance(firstLandingWaypoint.lat, firstLandingWaypoint.lon, (headingWind + 180), 0.1)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, secondLandingWaypoint.lat, secondLandingWaypoint.lon, 30))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstLandingWaypoint.lat, firstLandingWaypoint.lon, 30))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, latWind, lonWind, 30))

def takeoff(cmds, height):
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 0, 1, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 0, 1, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 10, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, 0, 0, 0, 17, 0, 0, 0, 0, height))



def rectangleMission(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight, cmds):

    finalPoint = pointRadialDistance(latWind, lonWind, headingWind, (distance + spaceDistance))

    # we're going to calculate the mission, we need some space for the takeoff of the drone and this space will be 500 meters and the width of the rectangle in this case will be 500m
    fase = rad2deg(math.atan((widthRectangle/2)/spaceDistance))
    print(fase)
    h = (widthRectangle/2)/math.sin(deg2rad(fase))
    print(h)
    firstLocation = pointRadialDistance(latFlight,lonFlight,(headingFlight + fase),h)
    firstLandingWaypoint = pointRadialDistance(latWind, lonWind, (headingWind + 180), 0.1)
    secondLandingWaypoint = pointRadialDistance(firstLandingWaypoint.lat, firstLandingWaypoint.lon, (headingWind + 180), 0.1)

    takeoff(cmds, height)
    
    #first point
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstLocation.lat, firstLocation.lon, height))


    print(finalPoint.lat, finalPoint.lon)
    print(firstLocation.lat, firstLocation.lon)

    #second point
    locationLoop = pointRadialDistance(firstLocation.lat, firstLocation.lon, headingFlight - 90, widthRectangle)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))

    division = (distance / spaceBtwLines) / 2 #
    print(division)
    print(locationLoop.lat, locationLoop.lon)

    for x in range(int(division)):
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight, spaceBtwLines)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight + 90, widthRectangle)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight, spaceBtwLines)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight - 90, widthRectangle)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_LAND_START, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, 50))

    landing(latWind,lonWind,headingWind,cmds)

    
    cmds.upload()

    return cmds