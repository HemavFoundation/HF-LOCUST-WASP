from adafruit_rockblock import RockBlock
# via USB cable
import serial
# uart = serial.Serial("COM5", 19200)
uart = serial.Serial("/dev/ttyUSB0", 19200)

rb = RockBlock(uart)

def check_connection():

    resp = rb._uart_xfer("+CSQ")

    if resp[-1].strip().decode() == "OK":
        status = int(resp[1].strip().decode().split(":")[1])

    else:
        quality = False

    signal_strength = status

    print("Signal strength:",signal_strength)

    if signal_strength >= 1:
        quality = True

    else:
        quality= False

    return quality


if __name__ == '__main__':

        cc = check_connection()

        while cc is not True:
            cc = check_connection()
            print("Checking again...")

        if cc is not False:

            print("Ready to send message!")