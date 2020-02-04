
import picamera
from picamera import PiCamera
import picamera.array
import cv2
import numpy as np


class CameraInterface:

    def __init__(self):
        self.camera = PiCamera()

        # With the maximum resolution takes about 10 seconds to process an image
        self.camera.resolution = (2528, 1968)
        # self.camera.resolution = (3280, 2464)
        # self.camera.resolution = (1640, 922)

        self.redAWB = 0.9
        self.blueAWB = 2.2
        
        customGains = (self.redAWB, self.blueAWB)
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = customGains

        self.camera.drc_strength = 'high'   #dynamic range of the camera
        self.camera.exposure_mode = 'auto'

        self.camera.brightness = 30

    def test_settings(self, num):

        if num >= 500:
            self.redAWB = 0.9
            self.blueAWB = 2.2
            self.camera.brightness = 30
            
        customGains = (self.redAWB, self.blueAWB)
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = customGains
    
    def capture_frame(self):     # capture frame and filters the image for vegetation detection

        img = np.empty((self.camera.resolution[1], self.camera.resolution[0], 3), dtype=np.uint8)

        self.camera.capture(img, 'bgr')
    # img = picamera.array.PiRGBArray(self.camera).array

        return img


    def save_image(self, newfile, image):

        cv2.imwrite(newfile, image)

        return

    def camera_settings(self):
        red_gain = self.redAWB
        blue_gain = self.blueAWB
        exposure = self.camera.exposure_mode
        brightness = self.camera.brightness

        settings = [red_gain, blue_gain, exposure, brightness]
        return settings






