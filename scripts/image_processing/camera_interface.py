import picamera
from picamera import PiCamera
import picamera.array
import cv2
import numpy as np
import json


class CameraInterface:

    def __init__(self):

        #First we need to initialize the monospectral camera and all the related settings
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


        #We initialize some other variables that has nothing related with camera settings

        self.results = []

    def test_settings(self, num):

        if num >= 0:
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
    

    def edit_json(self, newFlight):
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


    def write_json(self, timestamp, num, percentage, data_drone, image_settings, path):
        coordinates = (data_drone[0], data_drone[1])
        self.results.append(
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
            "results": self.results
        }

        return flight

    def tag_image(self, img, vertex_coordinates):
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

        return img





