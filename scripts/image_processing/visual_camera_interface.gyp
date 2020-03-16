"""
Created on Thu Mar 12 15:03 2020

This script contains the class that is in charge to control
everything related with the visual camera. 

Actions to be performed with the camera:
    1) Connect to the camera on the correct serial port (it may change)
    2) Set the camera settings 
    3) Take images and store them to be readable by the main program
    4) Save those images on the correct path 
    5) GPS coordinates are tagged directl on the image, not in the json file
    6) write all the image path and the name on the json file

To do so, we will work with the pygame library for controlling the camera and 
as well as with numpy and cv2 (the same as the other programs contained on that project)
"""

import os
import json
import pygame
import pygame.camera
from pygame.locals import *
import numpy as np
import cv2


class VisualCameraInterface:

    def __init__(self, timestamp, path_visualimages):

        # visual camera settings
        self.port = "/dev/video0"
        self.resolution = (640, 480)
        self.cam = pygame.camera.Camera(self.port, self.resolution)
        self.cam.start()
        
        # variables we need to introduce from the main script
        self.timestamp = timestamp
        self.path = path_visualimages

        # We initialize the array containing the data of the images
        self.visualimages = []


    def take_image(self):    #function to take an image with the visual image

        img = np.empty((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
        image = self.cam.get_image()
        img = cv2.imread(image)
        return img


    def edit_json(self, newvisualimage):
        # we try to write an existing json. If not existing, we create a new one
        try:
            with open('/home/pi/Desktop/HF-LOCUST-WASP/visual_images.json', 'r+') as f:
                data = []
                try:
                    data = json.load(f)
                except:
                    print("Empty json r+")

                data.append(newvisualimage)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                f.close()

        except:
            with open('/home/pi/Desktop/HF-LOCUST-WASP/visual_images.json', 'w') as f:
                data = []
                try:
                    data = json.load(f)
                except:
                    print("Empty json x")

                data.append(newvisualimage)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                f.close()

        print("done")


    def write_json(self, num_visual, path_visual):
        self.visualimages.append(
            {
                "image_id": num_visual,
                "image_path": path_visual,
            }
        )

        locust_images = {
            "id": self.timestamp,
            "results": self.visualimages
        }

        return locust_images

    def tag_image(self, img, coordinates):


        font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        org = (50, 50)
        # fontScale
        fontScale = 0.8

        # Blue color in BGR
        color = (255, 255, 255)

        # Line thickness of 2 px
        thickness = 2

        # Using cv2.putText() method
        cv2.putText(img, str(coordinates), org, font, fontScale, color, thickness, cv2.LINE_AA)
        return img

    def save_image(self, img, num):
        name = str(self.path) + '/' + str(num)
        cv2.imwrite(name, img)

    