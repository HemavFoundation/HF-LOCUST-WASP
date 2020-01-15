from dronekit import *



class AutopilotInterface():

    def __init__(self):
        #device = args.connect

        device = '/dev/ttyS0'
        #vehicle = connect(device, wait_ready=True, baud=57600)
        vehicle = connect(device, baud=921600, wait_ready=True)
        self.vehicle = vehicle

    # def connect_to_vehicle(self):
    #     # with mini USB: '/dev/ttyACM0'
    #     # with cable (telem2): '/dev/ttyAMA0'
    #     device = args.connect
    #
    #     vehicle = connect(device, wait_ready=True, baud=57600)
    #
    #     return vehicle

    # # #
    def set_data_drone(self):      # necessary data to tag the obtained vegetated images
        latitude = self.vehicle.location.global_frame.lat
        longitude = self.vehicle.location.global_frame.lon
        pitch = self.vehicle.attitude.pitch
        altitude = self.vehicle.location.global_frame.alt

        data_drone = [latitude, longitude, altitude, pitch]

        return data_drone

    def get_altitude(self):
        return self.vehicle.location.global_frame.alt

    # # #

    def get_latitude(self):
        try:
            print(self.vehicle.location.global_frame.lat)
        except:
            print("not able to get latitude")

        return self.vehicle.location.global_frame.lat

    # # #

    def get_longitude(self):
        try:
            print(self.vehicle.location.global_frame.lon)
        except:
            print("not able to get longitude")

        return self.vehicle.location.global_frame.lon

    # # #

    def get_heading(self):
        try:
            print(self.vehicle.heading)
        except:
            print("not able to get azimut")

        return self.vehicle.heading

    # # #

    def get_yaw(self):  # pan

        try:
            print(self.vehicle.attitude.yaw)
        except:
            print("not able to get yaw")

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
