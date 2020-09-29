import time
from adafruit_rockblock import RockBlock
import serial
import struct
import json
from config import *

class RockClient():
    def __init__(self):

        #self.rockblock_port = rockblock_settings['port']
        self.rockblock_port = "COM11"
        self.baudrate = rockblock_settings['baudrate']

    def check_connection(self, rb):

        resp = rb._uart_xfer("+CSQ")

        if resp[-1].strip().decode() == "OK":
            status = int(resp[1].strip().decode().split(":")[1])

        else:
            quality = False

        signal_strength = status

        print("Signal strength:", signal_strength)

        if signal_strength >= 1:
            quality = True

        else:
            quality = False

        return quality

    def connect_rockblock(self):
        # via USB cable
        print("Connected!")
        uart = serial.Serial(self.rockblock_port, self.baudrate)

        rb = RockBlock(uart)

        return rb

    def get_time(self):
        rb = self.connect_rockblock()
        resp = rb._uart_xfer("+CCLK?")  # 20/09/26,12:07:13

        if resp[-1].strip().decode() == "OK":
            status = tuple(resp[1].decode().split(","))
            date = (status[0].split(":"))[1]

            year = str(int(date.split("/")[0]) + 2000)
            month = date.split("/")[1]
            day = date.split("/")[2]

            time = status[1]
            hour = int(time.split(":")[0]) + 2 # UTC +2 for Spain
            min = time.split(":")[1]
            #sec = time.split(":")[2]

            timestamp = str(year) + "_" + str(month) + "_" + str(day) + "-" + str(hour) + "_" + str(min)
            return timestamp

    def write_message(self, altitude, latitude, longitude, heading, status):  
        data = ""
        #Short data:
        alt = round(altitude,1)
        lat = round(latitude,5)
        lon = round(longitude,5)
        id = drone_id.replace("-", "")

        #Select message construction type:
        if status == 0: #LANDING
            data = str(drone_id) + ',' + str(status) + ',' + str(latitude) + ',' + str(longitude) + ',' + str(alt)
       
        else status == 1: #FLIGHT
            data = str(drone_id) + ',' + str(status) + ',' + str(latitude) + ',' + str(longitude) + ',' + str(alt) + ','+ str(heading) + ','+ str(typeOfMission)

        return data

    def send_location(self, lat, lon, alt, hdg, status): 
 
        rb = self.connect_rockblock()

        cc = self.check_connection(rb)

        previous = time.perf_counter()
        timer = 0

        while cc is not True:
            current = time.perf_counter()
            timer += current - previous
            previous = current
            cc = self.check_connection(rb)
            print("Checking again...")

            if timer > 30:
                print('Im tired of checking signal')
                break

        if cc is not False:
            
            data = self.write_message(alt, lat, lon, hdg, status)

            print("Ready to send message!")

            # put data in outbound buffer
            rb.out_text = data

            # try a satellite Short Burst Data transfer
            print("Talking to satellite...")

            status = rb.satellite_transfer()

            # loop as needed
            retry = 0
            while status[0] > 8:
                time.sleep(10)
                status = rb.satellite_transfer()
                print("Try num:", retry)
                print("Satellite status:", status)
                retry += 1

            print("\nDONE.")
