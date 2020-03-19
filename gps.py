import serial
import time
import string
import pynmea2

port="/dev/ttyAMA0"
ser=serial.Serial(port, baudrate=9600, timeout=1)
dataout = pynmea2.NMEAStreamReader()
        
class GpsData:
    def __init__(self):
        pass
    def getLatLon(self):
        lat = -1
        lon = -1
        try:
            newdata=ser.readline()
            if newdata[0:6] == "$GPRMC":
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                lon=newmsg.longitude
                gps = "Latitude=" + str(lat) + "and Longitude=" + str(lon)
                print(gps)
                return([lat,lon])
        except Exception as e:
            print(e)
            return([-1,-1])
        
gpsObj = GpsData()
print(gpsObj.getLatLon())


# while True:
#     port="/dev/ttyAMA0"
#     ser=serial.Serial(port, baudrate=9600, timeout=1)
#     dataout = pynmea2.NMEAStreamReader()
#     try:
#         newdata=ser.readline()
#         if newdata[0:6] == "$GPRMC":
#             newmsg=pynmea2.parse(newdata)
#             lat=newmsg.latitude
#             lng=newmsg.longitude
#             gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
#             print(gps)
#     except Exception as e:
#         print(e)
