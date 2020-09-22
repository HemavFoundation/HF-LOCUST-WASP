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
from image_processing.visual_camera_interface import *
from image_processing.data_management import *
from commonFunctions import *
import numpy as np
import os
import json
import pandas as pd
import cv2
import math


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
    
    path_flight = path + "/" + timestamp
    
    try:
        os.mkdir(path_flight)
    except: 
        path_flight = path + "/" + timestamp + "_2"
        os.mkdir(path_flight)
    
    path_ndvi_images = path_flight + "/" + "ndvi_images"  # we create the string for the new directory
    path_display_photos = path_flight + "/" + "display_photos" 
    
    os.mkdir(path_ndvi_images)  # creates a directory
    os.mkdir(path_display_photos)

    raw_images = path_ndvi_images + "/" + "raw_images"
    os.mkdir(raw_images)

    return path_ndvi_images, path_display_photos, raw_images, timestamp


def contrast_stretch(im):
    """
    Performs a simple contrast stretch of the given image, from 1-100%.
    """
    in_min = np.percentile(im, 1)
    in_max = np.percentile(im, 100)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def main_loop_mono(num, newpath, raw_images_path, camera_interface, autopilot_interface, data_interface):
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

    median = cv2.bilateralFilter(ndvi_new, 3, 75, 75)
    ndvi_new = median

    # we apply some morphological operations to enhance vegetation

    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(ndvi_new, kernel, iterations=1)

    kernel = np.ones((2, 2), np.uint8)
    dilation = cv2.dilate(erosion, kernel, iterations=1)

    ndvi_new = dilation
    ndvi_values = np.count_nonzero(ndvi_new > 126)
    
    # once we have the final image with vegetation, we remove everything that is under 0.14 (163) NDVI value
    ndvi_new[ndvi_new < 163] = 0
    values_ndvi = np.count_nonzero(ndvi_new > 0)

    total_values = ndvi_new.shape[0] * ndvi_new.shape[1]

    percent = round(((ndvi_values / total_values) * 100), 2)

    if percent >= 0:

        name_ndvi = newpath + '/' + str(num) + '.jpeg'
        
        name = raw_images_path + '/' + str(num) + '.jpeg'
        # we save the raw image
        cv2.imwrite(name, img)

       
        # to create the final output, we want to add what is vegetation to the raw image

        mask_vegetation = cv2.inRange(ndvi_new, 163, 255)
        res = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask_vegetation))

        ndvi_final = cv2.cvtColor(ndvi_new, cv2.COLOR_GRAY2BGR)
        ndvi_result = cv2.bitwise_and(ndvi_final, ndvi_final, mask=mask_vegetation)

        # fusion is the final output, containing vegetation and original image
        fusion = res + ndvi_result

        # we want to tag each corner of the image with its real geographical coordinates

        tag_images = autopilot_interface.image_coordinates()
        
        coordinates = autopilot_interface.get_coordinates()
        heading = autopilot_interface.get_heading()

        img = fusion
        
        fusion = camera_interface.tag_image(img, coordinates, heading)

        cv2.imwrite(name_ndvi, fusion)

        # once we have saved the final output, we save interesting data on the json file

        data_drone = autopilot_interface.set_data_drone()

        image_settings = camera_interface.camera_settings()
        
        path_ndvi_json = '/results/photos/' + str(timestamp) + '/ndvi_images/' + str(num) + '.jpeg'
        
        flight_info = data_interface.write_json_vegetation(timestamp, num, percent, data_drone, path_ndvi_json)

        print('@@@ image processed @@@')
        return flight_info

    else:
        return None


def main_loop_visual(num, path, visualcamera_interface, autopilot_interface, data_interface):
    img = visualcamera_interface.take_image()

    path_visual_json = '/results/photos/' + str(timestamp) + '/display_photos/' + str(num) + '.jpeg'

    latitude = autopilot_interface.get_latitude()
    longitude = autopilot_interface.get_longitude()
    heading = autopilot_interface.get_heading()
    
    coordinates = (latitude, longitude)
    
    try:
        img = visualcamera_interface.tag_image(img, coordinates, heading)
    except: 
        print('Could not tag the image')
    
    flight_info = data_interface.write_json_visual(timestamp, num, path_visual_json)
    visualcamera_interface.save_image(path, img, num)

    return flight_info
