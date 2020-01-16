
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
   
        self.redAWB = 1.5
        self.blueAWB = 1.9
        self.camera.contrast = 20
        
        customGains = (self.redAWB, self.blueAWB)
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = customGains
        

        self.camera.drc_strength = 'off'   #dynamic range of the camera
        # self.camera.resolution = (3280, 2464)
        # self.camera.resolution = (1640, 922)

        self.camera.exposure_mode = 'auto'

        # camera.iso = 150
        # camera.shutter_speed = 150
        # camera.exposure_mode = 'off'
    def test_settings(self, num, ):
        
        if num < 20:
            self.redAWB = 1.5
            self.blueAWB = 1.9
            self.camera.contrast = 0
        
        if num >= 20 and num < 40:
            self.redAWB = 0.8
            self.blueAWB = 2.5
            self.camera.contrast = 20
            
        if num >= 40 and num < 60:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
            
        if num >= 60 and num < 80:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
            
        if num >= 80 and num < 100:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
            
        if num >= 100 and num < 120:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
        
        if num >= 120 and num < 140:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
        
        if num >= 140 and num < 160:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
            
        if num >= 160 and num < 180:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
        
        if num >= 180 and num < 200:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
        
        if num >= 200 and num < 220:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
        
        if num >= 220 and num < 240:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
        
        if num >= 240 and num < 260:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
        
        if num >= 260 and num < 280:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
            
        if num >= 280 and num < 300:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.contrast = 20
            
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
        brightness = self.camera.drc_strength

        settings = [red_gain, blue_gain, exposure, brightness]
        return settings






