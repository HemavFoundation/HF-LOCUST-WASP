
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

        self.camera.drc_strength = 'high'   #dynamic range of the camera
        # self.camera.resolution = (3280, 2464)
        # self.camera.resolution = (1640, 922)

        self.camera.exposure_mode = 'auto'

        # camera.iso = 150
        # camera.shutter_speed = 150
        # camera.exposure_mode = 'off'
    def test_settings(self, num):
        
        if num < 20:
            self.redAWB = 1.5 
            self.blueAWB = 1.9
            self.camera.brightness = 30
        
        if num >= 20 and num < 40:
            self.redAWB = 1.5 
            self.blueAWB = 1.9
            self.camera.brightness = 50
            
        if num >= 40 and num < 60:
            self.redAWB = 1.5 
            self.blueAWB = 1.9
            self.camera.brightness = 60
            
        if num >= 60 and num < 80:
            self.redAWB = 1.5 
            self.blueAWB = 1.9
            self.camera.brightness = 70
            
        if num >= 80 and num < 100:
            self.redAWB = 1.5 
            self.blueAWB = 1.9
            self.camera.brightness = 80
            
##############
            
        if num >= 100 and num < 120:
            self.redAWB = 0.5 
            self.blueAWB = 1.5
            self.camera.brightness = 30
        
        if num >= 120 and num < 140:
            self.redAWB = 0.5 
            self.blueAWB = 1.5
            self.camera.brightness = 50
            
        if num >= 140 and num < 160:
            self.redAWB = 0.5 
            self.blueAWB = 1.5
            self.camera.brightness = 60
            
        if num >= 160 and num < 180:
            self.redAWB = 0.5 
            self.blueAWB = 1.5
            self.camera.brightness = 70

        if num >= 180 and num < 200:
            self.redAWB = 0.5 
            self.blueAWB = 1.5
            self.camera.brightness = 80
        
###############
            
        if num >= 200 and num < 220:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.brightness = 30
        
        if num >= 220 and num < 240:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.brightness = 50
        
        if num >= 240 and num < 260:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.brightness = 60
        
        if num >= 260 and num < 280:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.brightness = 70
            
        if num >= 280 and num < 300:
            self.redAWB = 0.9
            self.blueAWB = 1.5
            self.camera.brightness = 80
            
###############
            
        if num >= 300 and num < 320:
            self.redAWB = 1.2
            self.blueAWB = 1.9
            self.camera.brightness = 30
            
        if num >= 320 and num < 340:
            self.redAWB = 1.2
            self.blueAWB = 1.9
            self.camera.brightness = 50
            
        if num >= 340 and num < 360:
            self.redAWB = 1.2
            self.blueAWB = 1.9
            self.camera.brightness = 60
            
        if num >= 360 and num < 380:
            self.redAWB = 1.2
            self.blueAWB = 1.9
            self.camera.brightness = 70
            
        if num >= 380 and num < 400:
            self.redAWB = 1.2
            self.blueAWB = 1.9
            self.camera.brightness = 80
            
########################
            
        if num >= 400 and num < 420:
            self.redAWB = 1.9
            self.blueAWB = 1.2
            self.camera.brightness = 30
            
        if num >= 420 and num < 440:
            self.redAWB = 1.9
            self.blueAWB = 1.2
            self.camera.brightness = 50
        
        if num >= 440 and num < 460:
            self.redAWB = 1.9
            self.blueAWB = 1.2
            self.camera.brightness = 60
            
        if num >= 460 and num < 480:
            self.redAWB = 1.9
            self.blueAWB = 1.2
            self.camera.brightness = 70
            
        if num >= 480 and num < 500:
            self.redAWB = 1.9
            self.blueAWB = 1.2
            self.camera.brightness = 80
            
########################
            
        if num >= 500 and num < 520:
            self.redAWB = 0.9
            self.blueAWB = 2.2
            self.camera.brightness = 30
            
        if num >= 520 and num < 540:
            self.redAWB = 0.9
            self.blueAWB = 2.2
            self.camera.brightness = 50
        
        if num >= 540 and num < 560:
            self.redAWB = 0.9
            self.blueAWB = 2.2
            self.camera.brightness = 60
            
        if num >= 560 and num < 580:
            self.redAWB = 0.9
            self.blueAWB = 2.2
            self.camera.brightness = 70
            
        if num >= 580 and num < 600:
            self.redAWB = 0.9
            self.blueAWB = 2.2
            self.camera.brightness = 80
            
########################
            
        if num >= 600 and num < 620:
            self.redAWB = 1.5
            self.blueAWB = 2.2
            self.camera.brightness = 30
            
        if num >= 620 and num < 640:
            self.redAWB = 1.5
            self.blueAWB = 2.2
            self.camera.brightness = 50
        
        if num >= 640 and num < 660:
            self.redAWB = 1.5
            self.blueAWB = 2.2
            self.camera.brightness = 60
            
        if num >= 660 and num < 680:
            self.redAWB = 1.5
            self.blueAWB = 2.2
            self.camera.brightness = 70
            
        if num >= 680 and num < 700:
            self.redAWB = 1.5
            self.blueAWB = 2.2
            self.camera.brightness = 80
            
########################
            
        if num >= 700 and num < 720:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 30
            
        if num >= 720 and num < 740:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 50
        
        if num >= 740 and num < 760:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 60
            
        if num >= 760 and num < 780:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 70
            
        if num >= 780 and num < 800:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 80
            
    ########################
            
        if num >= 800 and num < 820:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 30
            
        if num >= 820 and num < 840:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 50
        
        if num >= 840 and num < 860:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 60
            
        if num >= 860 and num < 880:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 70
            
        if num >= 880 and num < 900:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 80
            
########################
            
        if num >= 900 and num < 920:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 30
            
        if num >= 920 and num < 940:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 50
        
        if num >= 940 and num < 960:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 60
            
        if num >= 960 and num < 980:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 70
            
        if num >= 980 and num < 1000:
            self.redAWB = 1.5
            self.blueAWB = 0.9
            self.camera.brightness = 80
            
#######
            
        if num >= 1010 and num < 1020:
            self.redAWB = 1
            self.blueAWB = 1
            self.camera.brightness = 30
            
        if num >= 1020 and num < 1040:
            self.redAWB = 1
            self.blueAWB = 1
            self.camera.brightness = 50
        
        if num >= 1040 and num < 1060:
            self.redAWB = 1
            self.blueAWB = 1
            self.camera.brightness = 60
            
        if num >= 1060 and num < 1080:
            self.redAWB = 1
            self.blueAWB = 1
            self.camera.brightness = 70
            
        if num >= 1080 and num < 1100:
            self.redAWB = 1
            self.blueAWB = 1
            self.camera.brightness = 80

#########
            
        if num >= 1110 and num < 1120:
            self.redAWB = 1
            self.blueAWB = 1.2
            self.camera.brightness = 30
            
        if num >= 1120 and num < 1140:
            self.redAWB = 1
            self.blueAWB = 1.2
            self.camera.brightness = 50
        
        if num >= 1140 and num < 1160:
            self.redAWB = 1
            self.blueAWB = 1.2
            self.camera.brightness = 60
            
        if num >= 1160 and num < 1180:
            self.redAWB = 1
            self.blueAWB = 1.2
            self.camera.brightness = 70
            
        if num >= 1180 and num < 1200:
            self.redAWB = 1
            self.blueAWB = 1.2
            self.camera.brightness = 80
            
        if num > 1200:
            self.redAWB = 1
            self.blueAWB = 1
            self.camera.brightness = 50
            
            
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






