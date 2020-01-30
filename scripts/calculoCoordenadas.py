from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil

def deg2rad(angle):
    return angle*pi/180


def rad2deg(angle):
    return angle*180/pi

def get_location_metres(lat, lon, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned Location has the same `alt` value
    as `original_location`.
    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*lat/180))

    #New position in decimal degrees
    newlat = lat + (dLat * 180/math.pi)
    newlon = lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,0)

def get_secondloc(lat, lon, heading, distance):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned Location has the same `alt` value
    as `original_location`.
    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth

    ad = distance/earth_radius
    
    lat2 = math.asin((math.sin(lat)*math.cos(ad))+(math.cos(lat)*math.sin(ad)*math.cos(heading)))
    lon2 = lon + math.atan2(math.sin(heading)*math.sin(ad)*math.cos(lat), math.cos(ad) - (math.sin(lat)*math.sin(lat2)))

    
    return LocationGlobal(lat2, lon2,0)

newCoo = get_secondloc(17.97689,-15.522684,80,5000)

print(newCoo.lat)
print(newCoo.lon)