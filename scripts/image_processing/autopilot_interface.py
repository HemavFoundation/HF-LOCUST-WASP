from dronekit import *



class AutopilotInterface():

    def __init__(self, vehicle):
        
        device = '/dev/ttyS0'
        #vehicle = connect(device, wait_ready=True, baud=57600)
#       vehicle = connect(device, baud=921600, wait_ready=True)
        self.vehicle = vehicle

    
    def set_data_drone(self):      # necessary data to tag the obtained vegetated images
        latitude = self.vehicle.location.global_frame.lat
        longitude = self.vehicle.location.global_frame.lon
        pitch = self.vehicle.attitude.pitch
        altitude = self.vehicle.location.global_frame.alt

        data_drone = [latitude, longitude, altitude, pitch]

        return data_drone

    def image_coordinates(self):
        latitude = self.vehicle.location.global_frame.lat
        longitude = self.vehicle.location.global_frame.lon
        heading = self.vehicle.heading
        pitch = self.vehicle.attitude.pitch
        altitude = self.vehicle.location.global_frame.alt
        roll = self.vehicle.attitude.roll

        coordinates = [latitude, longitude]
        tag_images = [coordinates, heading, altitude, pitch, roll]

        return tag_images

    def get_coordinates(self):
        latitude = self.vehicle.location.global_frame.lat
        longitude = self.vehicle.location.global_frame.lon

        coordinates = [latitude, longitude]
        return coordinates

    def get_altitude(self):
        return self.vehicle.location.global_relative_frame.alt

    def get_armed(self):
        return self.vehicle.armed

    # # #

    def get_latitude(self):
        return self.vehicle.location.global_frame.lat

    # # #

    def get_longitude(self):
        return self.vehicle.location.global_frame.lon

    # # #

    def get_heading(self):
        return self.vehicle.heading

    # # #

    def get_yaw(self):  # pan
        return self.vehicle.attitude.yaw

    def get_pitch(self):  # tilt

        try:
            print(self.vehicle.attitude.pitch)

        except:
            print("not able to get pitch")

        return self.vehicle.attitude.pitch

    # # #

    def get_roll(self):  # roll

        try:
            print(self.vehicle.attitude.roll)
        except:
            print("not able to get roll")

        return self.vehicle.attitude.roll

