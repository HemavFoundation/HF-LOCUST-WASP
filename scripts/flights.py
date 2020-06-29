from commonFunctions import *
from dronekit import *
from config import *
from math import asin,cos,pi,sin
from math import *


def landing(latWind, lonWind, headingWind, cmds):
    landpoint = pointRadialDistance(latWind,lonWind, headingWind, 0.04)
    firstLandingWaypoint = pointRadialDistance(latWind, lonWind, (headingWind + 180), 0.1)
    secondLandingWaypoint = pointRadialDistance(firstLandingWaypoint.lat, firstLandingWaypoint.lon, (headingWind + 180), 0.1)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, secondLandingWaypoint.lat, secondLandingWaypoint.lon, 50))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstLandingWaypoint.lat, firstLandingWaypoint.lon, 40))
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, landpoint.lat, landpoint.lon, 30))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, landpoint.lat, landpoint.lon, 30))


def takeoff(cmds, height):

    height = 50
    
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 0, 1, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_HOME, 0, 0, 1, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 10, 0, 0, 0, 0, 0, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, 0, 0, 0, 17, 0, 0, 0, 0, height))



def rectangleMission_reversed(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight, cmds):
    # we're going to calculate the mission, we need some space for the takeoff of the drone and this space will be 500 meters and the width of the rectangle in this case will be 500m
    fase = rad2deg(math.atan((widthRectangle/2)/(spaceDistance + distance)))
    print(fase)
    
    #h = (widthRectangle/2)/math.sin(deg2rad(fase))
    h = math.hypot(widthRectangle/2, spaceDistance + distance)
    print(h)
    
    finalPoint = pointRadialDistance(latFlight, lonFlight, (headingFlight - fase), h)
    firstLocation = pointRadialDistance(latFlight,lonFlight,(headingFlight + fase),h)
    
    firstLandingWaypoint = pointRadialDistance(latWind, lonWind, (headingWind + 180), 0.1)
    secondLandingWaypoint = pointRadialDistance(firstLandingWaypoint.lat, firstLandingWaypoint.lon, (headingWind + 180), 0.1)

    takeoff(cmds, height)
    
    #first point
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, finalPoint.lat, finalPoint.lon, height))


    print(finalPoint.lat, finalPoint.lon)
    print(firstLocation.lat, firstLocation.lon)

    #second point
    locationLoop = pointRadialDistance(finalPoint.lat, finalPoint.lon, headingFlight + 90, widthRectangle)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))

    division = (distance / spaceBtwLines) / 2 #
    print(division)
    print(locationLoop.lat, locationLoop.lon)

    for x in range(int(division)):
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight + 180, spaceBtwLines)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight - 90, widthRectangle)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight + 180, spaceBtwLines)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight + 90, widthRectangle)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))
        print (locationLoop.lat,locationLoop.lon)

    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_LAND_START, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, 50))

    landing(latWind,lonWind,headingWind,cmds)

    
    cmds.upload()

    return cmds


def rectangleMission_normal(latWind, lonWind, headingWind, distance, spaceDistance, widthRectangle, spaceBtwLines, height, latFlight, lonFlight, headingFlight, cmds):

    finalPoint = pointRadialDistance(latFlight, lonFlight, headingFlight, (distance + spaceDistance))

    # we're going to calculate the mission, we need some space for the takeoff of the drone and this space will be 500 meters and the width of the rectangle in this case will be 500m
    fase = rad2deg(math.atan((widthRectangle/2)/spaceDistance))
    print(fase)
    #h = (widthRectangle/2)/math.sin(deg2rad(fase))
    h = math.hypot(widthRectangle/2, spaceDistance)
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

def straightMission(latWind, lonWind, headingWind, distance, spaceDistance, height, latFlight, lonFlight, headingFlight, cmds):
    
    finalPoint = pointRadialDistance(latFlight, lonFlight, headingFlight, distance + spaceDistance)

    takeoff(cmds, height)
    
    #first point
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latWind, lonWind, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, finalPoint.lat, finalPoint.lon, height))


    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_LAND_START, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, 50))

    landing(latWind,lonWind,headingWind,cmds)    
    cmds.upload()

    return cmds



def periscopeMission(latWind, lonWind, headingWind, height, latFlight, lonFlight, cmds):

    radius = 0.1 # we need to have the radius variable in km
    wp_number = 10  # we define the number of wp we will have on one loop

    angle_between_wp = round((360 / wp_number), 1)

    takeoff(cmds, height)

    number_turns = 2 * 360 

    counter_angle = 0

    while counter_angle <= number_turns:

        locationLoop = pointRadialDistance(latFlight,lonFlight, counter_angle, radius)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))

        counter_angle += angle_between_wp    

    landing(latWind,lonWind,headingWind,cmds)

    cmds.upload()

    return cmds
 
'''
def periscopeMission(latWind, lonWind, headingWind, height, latFlight, lonFlight, cmds):

    radius = 150 # we need to have the radius variable in km
    wp_number = 6  # we define the number of wp we will have on one loop

    angle_between_wp = round((360 / wp_number), 1)

    takeoff(cmds, height)

    number_turns = 2  

    counter_angle = 0

    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TURNS, 0, 0, number_turns, 0, radius, 0, latFlight, lonFlight, height))

    landing(latWind,lonWind,headingWind,cmds)

    cmds.upload()

    return cmds
'''

def ZigZagMission(latWind, lonWind, headingWind, distance, spaceDistance, spaceBtwPeaks, width, height, latFlight, lonFlight, headingFlight, cmds):
    
    finalpoint = pointRadialDistance(latFlight, lonFlight, headingFlight, (distance + spaceDistance))
    fase = rad2deg(math.atan((width/2)/spaceDistance))
    hTakeOff = math.hypot((width/2),spaceDistance)

    faseDiagonal = rad2deg(math.atan(width/spaceBtwPeaks))
    hZigZag = math.hypot(width,spaceDistance)

    firstlocation = pointRadialDistance(latFlight,lonFlight,(headingFlight + fase), hTakeOff)

    firstLandingWaypoint = pointRadialDistance(latWind, lonWind, (headingWind + 180), 0.1)
    secondLandingWaypoint = pointRadialDistance(firstLandingWaypoint.lat, firstLandingWaypoint.lon, (headingWind + 180), 0.1)

    takeoff(cmds, height)
    print("Taken off, initialazing mission")
    # Volvemos a pasar por encima del punto de despegue para corregir la trayectoria de la linea recta
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    
    #Empezamos el zig-zag
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstlocation.lat, firstlocation.lon, height))
    
    #Second point
    locationLoop = pointRadialDistance(firstlocation.lat, firstlocation.lon, headingFlight - faseDiagonal, hZigZag)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))


    x = spaceBtwPeaks

    while x<distance:
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight + faseDiagonal, hZigZag)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))

        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, headingFlight - faseDiagonal, hZigZag)
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, locationLoop.lat, locationLoop.lon, height))

        
        x= x+ (2*spaceBtwPeaks)
    
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_LAND_START, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, 50))

    landing(latWind, lonWind, headingWind, cmds)

    cmds.upload()

    return cmds

def ZigZagMissionInversed(latWind, lonWind, headingWind, distance, spaceDistance, spaceBtwPeaks, width, height, latFlight, lonFlight, headingFlight, cmds):

    firstpoint = pointRadialDistance(latFlight, lonFlight, headingFlight, distance)

    takeoff(cmds, height)
    print("Taken off, initialazing mission")

    # straight line to first point
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latWind, lonWind, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstpoint.lat, firstpoint.lon, height))
    print("Arrived at first point, initializing come-back")

    # then start zig-zag but inversed way
    finalpoint = LocationGlobal(latFlight, lonFlight, 0)
    headingFlight = -headingFlight
    alpha = rad2deg(math.atan(spaceBtwPeaks/(2*width)))
    print("Angle of diagonal: ", alpha)
    diagonalDist = math.hypot((spaceBtwPeaks/2),width)
    print("Length of the diagonal:", diagonalDist)

    firstlocation = pointRadialDistance(firstpoint.lat,firstpoint.lon,(headingFlight+90-alpha),(diagonalDist/2))
    #second location
    lastlocation = pointRadialDistance(firstlocation.lat,firstlocation.lon,(headingFlight-90+alpha),diagonalDist)
    
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, firstlocation.lat, firstlocation.lon, height))
    cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, lastlocation.lat, lastlocation.lon, height))

    x = (spaceBtwPeaks/4)+(spaceBtwPeaks/2) #lo que hemos recorrido ya
    while x<distance:
        nextlocation = pointRadialDistance(lastlocation.lat,lastlocation.lon,(headingFlight+90-alpha),diagonalDist)
        cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, nextlocation.lat, nextlocation.lon, height))
        print(nextlocation.lat,nextlocation.lon)

        nextnextlocation = pointRadialDistance(nextlocation.lat,nextlocation.lon,(headingFlight-90+alpha),diagonalDist)
        cmds.add(Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, nextnextlocation.lat, nextnextlocation.lon, height))
        print(nextnextlocation.lat,nextnextlocation.lon)

        lastlocation.lat = nextnextlocation.lat
        lastlocation.lon = nextnextlocation.lon
        
        x=x+spaceBtwPeaks

    # start landing
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_LAND_START, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, height))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 0, 0, 0, 0, 0, latFlight, lonFlight, 50))

    landing(latWind,lonWind,headingWind,cmds)

    cmds.upload()

    return cmds
