"""
Created on Thu Nov 14 11:30 2019

This code has to recognise vegetation in the dessert using a NIR raspberry pi camera and processing images with a raspberry.

For this reason, we need:
    1) Connect the camera to the raspberry and the raspberry to the Pixhawk
    2) Take images every XXX seconds
    3) Split the image in the 3 bands. for each image, we will obtain 3 arrays. By operating with this arrays, we compute the NDVI
    4) If the NDVI is higher that XXX value, we need to connect contact the pixhawk in order to obtain GPS data.
    5) A txt file should be generated will all the necessary data or the application

"""

from image_processing.autopilot_interface import *
from image_processing.camera_interface import *
import numpy as np
import os
import json
import pandas as pd
import cv2
import math
global results

results = []

def edit_json(newFlight):
    # we try to write an existing json. If not existing, we create a new one
    try:
        with open('/home/pi/Desktop/HF-LOCUST-WASP/results.json', 'r+') as f:
            data = []
            try:
                data = json.load(f)
            except:
                print("Empty json r+")

            data.append(newFlight)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()

    except:
        with open('/home/pi/Desktop/HF-LOCUST-WASP/results.json', 'w') as f:
            data = []
            try:
                data = json.load(f)
            except:
                print("Empty json x")

            data.append(newFlight)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()

    print("done")


def write_json(timestamp, num, percentage, data_drone, image_settings, path):
    coordinates = (data_drone[0], data_drone[1])
    results.append(
        {
            "image_id": num,
            "percentage": percentage,
            "coordinates": coordinates,
            "image_path": path,
            "camera_settings": image_settings,
        }
    )

    flight = {
        "id": timestamp,
        "results": results
    }

    return flight


def create_directory():  # tested and working

    path = '/home/pi/Desktop/HF-LOCUST-WASP/public/results/photos'
    # we need to convert numbers to string to be able to create the new path
    year = str(pd.datetime.now().year)
    month = str(pd.datetime.now().month)
    day = str(pd.datetime.now().day)
    hour = str(pd.datetime.now().hour)
    minute = str(pd.datetime.now().minute)
    global timestamp

    timestamp = year + "_" + month + "_" + day + "-" + hour + "_" + minute
    newpath = path + "/" + timestamp  # we create the string for the new directory

    os.mkdir(newpath)  # creates a directory
    normal_images = newpath + '/' + 'raw_images'
    ndvi_images = newpath + '/' + 'ndvi_images'
    os.mkdir(normal_images)
    os.mkdir(ndvi_images)

    return newpath


def contrast_stretch(im):
    """
    Performs a simple contrast stretch of the given image, from 5-95%.
    """
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out


def getEndpoint(image_coordinates, bearing, d):
    lat1 = image_coordinates[0]
    lon1 = image_coordinates[1]

    R = 6371 * 1000  # Radius of the Earth in meters

    brng = math.radians(bearing)  # convert degrees to radians
    lat1 = math.radians(lat1)  # Current lat point converted to radians
    lon1 = math.radians(lon1)  # Current long point converted to radians

    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) + math.cos(lat1) * math.sin(d / R) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

    lat2 = round(math.degrees(lat2), 6)
    lon2 = round(math.degrees(lon2), 6)

    coordinates2 = [lat2, lon2]

    return coordinates2


def get_coordinates(coordinates, heading, h, pitch, roll):
    # CAMERA PARAMETERS

    # Sensor (mm)
    sx = 3.674
    sy = 2.76
    # Focal length of lens (mm)
    fl = 3.04
    # Pixels
    px = 1920
    py = 1080
    pixels_camera = px * py

    # Field of view wide (gra)
    HFOVcal = 2 * math.atan(sx / (2 * fl))
    VFOVcal = 2 * math.atan(sy / (2 * fl))

    print('@@@HORIZONTAL', HFOVcal)
    print('@@@@ Vertical', VFOVcal)
    # Now we need the airplane attitude data
    pitch = math.radians(pitch)
    roll = math.radians(roll)

    # FOOTPRINT(m) (by the moment considering no roll)

    drone_bottom = h * math.tan(pitch - 0.5 * VFOVcal)
    drone_top = h * math.tan(pitch + 0.5 * VFOVcal)
    drone_center = h * math.tan(pitch)

    d1 = drone_top - drone_center
    d2 = drone_center - drone_bottom

    fy = drone_top - drone_bottom
    fx = h * (math.tan(roll + 0.5 * HFOVcal) - math.tan(roll - 0.5 * HFOVcal))
    footprint = fy * fx

    print('@@@ footprint y', fy)
    print('@@@@ footprint x', fx)

    # Front left vertex
    diagonal1 = math.hypot(d1, fx / 2)
    orientation = heading - math.degrees(math.atan((fx / 2) / d1))
    fl_coordinates = getEndpoint(coordinates, orientation, diagonal1)
    print('@@@@ orientation 1', orientation)

    # Front right vertex
    diagonal = math.hypot(d1, fx / 2)
    orientation = heading + math.degrees(math.atan((fx / 2) / d1))
    fr_coordinates = getEndpoint(coordinates, orientation, diagonal)
    print('@@@@ orientation 2', orientation)

    # Back left vertex
    diagonal2 = math.hypot(d2, fx / 2)
    orientation = -heading + math.degrees(math.atan(d2 / (fx / 2)))
    bl_coordinates = getEndpoint(coordinates, orientation, diagonal2)
    print('@@@@ orientation 3', orientation)

    # Back right vertex
    diagonal = math.hypot(d2, fx / 2)
    orientation = -heading - math.degrees(math.atan(d2 / (fx / 2)))
    br_coordinates = getEndpoint(coordinates, orientation, diagonal)
    print('@@@@ orientation 4', orientation)

    vertex_coordinates = [fl_coordinates, fr_coordinates, bl_coordinates, br_coordinates]

    return vertex_coordinates


def main_loop(vehicle, num, newpath, camera_interface, autopilot_interface):
    img = camera_interface.capture_frame()

    # Once we have the original image, we need to take the red and nir channels to operate with them

    b = np.array(img[:, :, 0]).astype(float) + 0.00000000001
    r = np.array(img[:, :, 2]).astype(float) + 0.00000000001

    # we want to delete shadows from the original image, as they are introducing distorsions
    lower_limit = np.array([3, 3, 3])
    upper_limit = np.array([255, 255, 255])
    shadows = cv2.inRange(img, lower_limit, upper_limit)

    # using the blue filter, red channel is NIR band and blue channel is visible light

    kernel = np.ones((1, 1), np.uint8)
    dilation = cv2.dilate(r, kernel, iterations=10)
    nir = dilation
    red = b

    np.seterr(divide='ignore', invalid='ignore')

    # we compute the ndvi
    ndvi = ((nir - red) / (nir + red)).astype(float)

    # once we have the ndvi in (-1, 1) scale, we convert it to 0-255 scale to operate with opencv

    ndvi_contrasted = contrast_stretch(ndvi).astype(np.uint8)

    # we delete the shadows from the ndvi re-scaled image
    ndvi_new = cv2.bitwise_or(ndvi_contrasted, ndvi_contrasted, mask=shadows)

    median = cv2.bilateralFilter(ndvi_new, 10, 75, 75)
    ndvi_new = median

    # we apply some morphological operations to enhance vegetation

    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(ndvi_new, kernel, iterations=1)

    kernel = np.ones((2, 2), np.uint8)
    dilation = cv2.dilate(erosion, kernel, iterations=1)

    ndvi_new = dilation

    # once we have the final image with vegetation, we remove everything that is under 0.14 (163) NDVI value
    ndvi_new[ndvi_new < 163] = 0
    values_ndvi = np.count_nonzero(ndvi_new > 0)

    total_values = ndvi_new.shape[0] * ndvi_new.shape[1]

    percent = round(((values_ndvi / total_values) * 100), 2)

    if percent >= 5:

        name = newpath + '/' + 'raw_images' + '/' + str(num) + '.jpeg'
        name_ndvi = newpath + '/' + 'ndvi_images' + '/' + str(num) + '.jpeg'

        # name = path + '/' + 'ndvi_results' + '/' + 'image' + 'ndvi' + str(percent) + '.jpeg'

        # we save the raw image
        cv2.imwrite(name, img)

        # median = cv2.bilateralFilter(ndvi_final, 10, 75, 75)
        # ndvi_final = median
        # to create the final output, we want to add what is vegetation to the raw image

        mask_vegetation = cv2.inRange(ndvi_new, 163, 255)
        res = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask_vegetation))

        ndvi_final = cv2.cvtColor(ndvi_new, cv2.COLOR_GRAY2BGR)
        ndvi_result = cv2.bitwise_and(ndvi_final, ndvi_final, mask=mask_vegetation)

        # fusion is the final output, containing vegetation and original image
        fusion = res + ndvi_result

        # we want to tag each corner of the image with its real geographical coordinates

        tag_images = autopilot_interface.image_coordinates()
        vertex_coordinates = get_coordinates(tag_images[0], tag_images[1], tag_images[2], tag_images[3], tag_images[4])

        img = fusion
        font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        org = (50, 50)
        # fontScale
        fontScale = 0.5

        # Blue color in BGR
        color = (255, 255, 255)

        # Line thickness of 2 px
        thickness = 1

        # Using cv2.putText() method
        cv2.putText(img, str(vertex_coordinates[0]), org, font, fontScale, color, thickness, cv2.LINE_AA)
        # org
        org = (img.shape[1] - 230, 50)
        cv2.putText(img, str(vertex_coordinates[1]), org, font, fontScale, color, thickness, cv2.LINE_AA)
        # org
        org = (50, img.shape[0] - 50)
        cv2.putText(img, str(vertex_coordinates[2]), org, font, fontScale, color, thickness, cv2.LINE_AA)
        # org
        org = (img.shape[1] - 230, img.shape[0] - 50)
        cv2.putText(img, str(vertex_coordinates[3]), org, font, fontScale, color, thickness, cv2.LINE_AA)

        fusion = img

        cv2.imwrite(name_ndvi, fusion)

        # once we have saved the final output, we save interesting data on the json file

        data_drone = autopilot_interface.set_data_drone()

        image_settings = camera_interface.camera_settings()

        path_json = '/results/photos/' + str(timestamp) + '/' + 'raw_images' + '/' + str(num) + '.jpeg'
        flight_info = write_json(timestamp, num, percent, data_drone, image_settings, path_json)

        print('@@@ image processed @@@')
        return flight_info

    else:

        name = newpath + '/' + 'raw_images' + '/' + str(num) + '.jpeg'

        # name = path + '/' + 'ndvi_results' + '/' + 'image' + 'ndvi' + str(percent) + '.jpeg'

        cv2.imwrite(name, img)
        return None


# def main(vehicle):
#     global num
#     num = 1
#     camera_interface = CameraInterface()
#     autopilot_interface = AutopilotInterface(vehicle)
#     newpath = create_directory()
#     flight_data = None
# 
#     while vehicle.armed is True:
# 
#         altitude = autopilot_interface.get_altitude()
# 
#         if altitude >= 50:
#             flight_data = main_loop(vehicle, num, newpath, camera_interface, autopilot_interface)
#             camera_interface.test_settings(num)
#             num += 1
# 
#     if flight_data is not None:
#         try:
#             edit_json(flight_data)
#         except:
#             print("No flight")
# 
#     else:
#         print('Flight data is empty')
