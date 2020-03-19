import serial
import time
import string
import pynmea2
import socket

# $ sudo apt-get install python-rpi.gpio python3-rpi.gpio
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep
# Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW) # pin used 3-VCC 9-GND


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)



while True:
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()
#     print(newdata[0:6].decode("utf-8") )
    try:
        if newdata[0:6].decode("utf-8") == "$GPRMC":
            newmsg=pynmea2.parse(newdata.decode("utf-8"))
            lat=newmsg.latitude
            lng=newmsg.longitude
            print(lat,lng)
            if(lat == 0 or lng == 0):
                GPIO.output(3, GPIO.HIGH)
            else:
                GPIO.output(3, GPIO.LOW)
                
            message = str(lat)+","+str(lng)
            sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    #         gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
    #         print(gps)
    except:
        sock.sendto("-1,-1".encode(), (UDP_IP, UDP_PORT))

            
