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

    finalPoint = pointRadialDistance(lat1, lon1, bearing, (distance + 0.5))

    # we're going to calculate the mission, we need some space for the takeoff of the drone and this space will be 500 meters and the width of the rectangle in this case will be 500m
    fase = rad2deg(math.atan((widthRectangle/2)/spaceDistance))
    print(fase)
    h = (widthRectangle/2)/math.sin(deg2rad(fase))
    print(h)
    firstLocation = pointRadialDistance(lat1,lon1,(bearing + fase),h)
    print(finalPoint.lat, finalPoint.lon)
    print(firstLocation.lat, firstLocation.lon)
    locationLoop = pointRadialDistance(firstLocation.lat, firstLocation.lon, bearing - 90, widthRectangle)
    print(locationLoop.lat, locationLoop.lon)

    for x in range(10):
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, bearing, distance/20)
        print (locationLoop.lat,locationLoop.lon)
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, bearing + 90, widthRectangle)
        print (locationLoop.lat,locationLoop.lon)
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, bearing, distance/20)
        print (locationLoop.lat,locationLoop.lon)
        locationLoop = pointRadialDistance(locationLoop.lat,locationLoop.lon, bearing - 90, widthRectangle)
        print (locationLoop.lat,locationLoop.lon)
    

        
    
 
flight(18.023358,-15.944138,197,10,0.5,0.5)


