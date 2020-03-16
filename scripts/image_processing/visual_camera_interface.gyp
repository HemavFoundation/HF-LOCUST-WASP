"""
Created on Thu Mar 12 15:03 2020

This script contains the class that is in charge to control
everything related with the visual camera. 

Actions to be performed with the camera:
    1) Connect to the camera on the correct serial port (it may change)
    2) Set the camera settings 
    3) Take images and store them to be readable by the main program
    4) Save those images on the correct path 
    5) write all the needed information in the corresponding json file

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

    def __init__(self, num_visual, timestamp, data_drone, path_visualimages):

        # visual camera settings
        self.port = "/dev/video0"
        self.resolution = (640, 480)
        self.cam = pygame.camera.Camera(self.port, self.resolution)
        self.cam.start()
        
        # variables we need to introduce from the main script
        self.num = num_visual
        self.timestamp = timestamp
        self.data_drone = data_drone
        self.path = path_visualimages


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


    def write_json(self):
        coordinates = (self.data_drone[0], self.data_drone[1])
        visualimages.append(
            {
                "image_id": self.num,
                "coordinates": coordinates,
                "image_path": self.path,
            }
        )

        locust_images = {
            "id": self.timestamp,
            "results": visualimages
        }

        return locust_images


    def save_image(self):
        name = str(self.path_visualimages) + '/' + str(self.num)
        cv2.imwrite(name, )

    