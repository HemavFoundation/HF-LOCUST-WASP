import time
from adafruit_rockblock import RockBlock
import serial
import struct
import json
from config import *

class RockClient():
    def __init__(self):

        self.rockblock_port = rockblock_settings['port']
        #self.rockblock_port = "COM5"
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

    def write_message(self, alt, lat, lon):  # Aqui se codificará el mensaje para enviar
        typ = '1'
        status = '01'
        print(type(lat))
        datadict = {'lat': lat, 'lon': lon,
                    'alt:': alt, 'typ': typ, 'status': status}
        datajson = json.dumps(datadict).encode('utf-8')
        format = str(len(datajson)) + "s"
        datastruct = struct.pack(format, datajson)

        return datastruct


    def send_location(self, lat, lon, alt, heading):  # Aqui se enviarán los mensajes
        
        print('Satellite heading:', heading)
        rb = self.connect_rockblock()

        cc = self.check_connection(rb)

        previous = time.perf_counter()
        timer = 0

        while cc is not True:
            current = time.perf_counter()
            timer += current - previous
            cc = self.check_connection(rb)
            print("Checking again...")

            previous = current
            if timer > 30:
                break


        if cc is not False:
            data = self.write_message(alt,lat,lon, heading)

            print("Ready to send message!")

            # put data in outbound buffer
            rb.data_out = data

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
