# This code is TCU side implementation for geo-fence detection
# Written and maintained by probhakar, 19th March, 2020

import geo_fence_detector as gfd
import requests
import json
from datetime import datetime
from file_handler import updateGeofenceDataBase, getGeoFenceToMonitor, pointParser
import time
from utils import Point
import socket

# configuring UDP port for receiving gps in
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
# sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))

def getTimestamp(): 
    timestamp = int(datetime.timestamp(datetime.now())) + (5*60*60) + (30*60) # indian timezone
    return timestamp
# proxies = {
#     "http": "http://298115:Apr-2020@msilproxy.corp.maruti.co.in:65527",
#     "https": "https://298115:Apr-2020@msilproxy.corp.maruti.co.in:65527",
# }
proxies = {}

# url = "http://cat95.pythonanywhere.com/vehicleLatestLocation"
# data = {'IAM':'user', 'IAMKey':'u1w44Sn2oi1ujgo8KlXEQ817U', 'moID':'111111111111111'}
# r = requests.post(url, data=data, proxies = proxies)
# # {'timestamp': '1584580224', 'latutude': '28.4985869231', 'longitude': '77.0502026752'}
# data = r.json()
lat = 28.495773336584882
lon = 77.07199977755778

geoFenceBreachStatus = [] # geFenceID , isInside = false, GeoFenceDetectorPolygonObject

def initializeGeoFenceStatusListner():
    geoFences = getGeoFenceToMonitor()
    if(geoFences != 'error' and len(geoFences) > 0):
        for i in geoFences:
            geoFenceBreachStatus.append([i[0], False, gfd.GeoFenceDetectorPolygon(i[2])])


def sendToServerAndUpdateGeoFenceStack(timestamp, lat=28.495773336584882, lon =77.07199977755778):
    retryCount = 3
    while (retryCount > 0):
        try:
            data = {'IAM':'TCU', 
                'IAMKey':'YY6V2Gfc1B0C6nvOxi8ME53L4', 
                'moID':'111111111111111',
                'timestamp': timestamp,
                'sessionID': 0,
                'software_version': 1.0,
                'altitude': 0,
                'latitude': lat,
                'longitude': lon,
                'hdop': 0,
                'numsat': 0,
                'speed': 0,
                'ignition_status': 0,
                'ERS': 0,
                'steering_angle': 0,
                'ACOx': 0,
                'ACOy': 0,
                'ACOz': 0,
                'Roll': 0,
                'Pitch': 0,
                'Yaw': 0,
                'DTN': 0,
                'DITT': 0
            }
            r = requests.post("http://cat95.pythonanywhere.com/dataUpload", data=data, proxies = proxies)
            data = r.json()['pendingGeoFence']
            # print(data)
            print('$ data updated succesfully')
            dataToUpdate = []
            if(len(data) > 0): # that means there are geo-fences needs to be updated
                for i in data:
                    dataToUpdate.append([ i['geoFenceID'], i['geFenceType'], i['geoFencePoints']])
            print(dataToUpdate)
            s = updateGeofenceDataBase(dataToUpdate, False)
            # print(s)
            if(len(s)>0):
                try:
                    forWhom = "["+'"'+s[0]+'"'
                    for i in s[1:]:
                        forWhom += ","+'"'+i+'"'
                    forWhom += "]"
                    print(forWhom)
                    data = {'IAM':'TCU', 'IAMKey':'YY6V2Gfc1B0C6nvOxi8ME53L4', 'moID':'111111111111111', 'updateStatusFor': forWhom}
                    r = requests.post("http://cat95.pythonanywhere.com/updateGeofenceStatus", data=data, proxies = proxies)
                    print('$ geo-fence updated succesfully')
                    updateGeofenceDataBase(dataToUpdate, True)
                    geoFenceBreachStatus.append([i['geoFenceID'], False, gfd.GeoFenceDetectorPolygon(pointParser(i['geoFencePoints']))])
                except:
                    pass
            return 
        except Exception as e:
            print(e)
            print('retrying...')
            retryCount -= 1

def notifyServer(notificationID, notificationType, message):
    # notifyServer
    retryCount = 2
    while(retryCount > 0):
        try:
            data = {'IAM':'TCU', 
                'IAMKey':'YY6V2Gfc1B0C6nvOxi8ME53L4', 
                'moID':'111111111111111',
                    'notificationID': notificationID,
                    'notificationType': notificationType,
                    'details': message}
            r = requests.post("http://cat95.pythonanywhere.com/notifyServer", data=data, proxies = proxies)
            data = r.json()
            print(data)
            return
        except Exception as e:
            print(e)
            retryCount -= 1
        
        
        
  
# for the first time
flag = True
while(True):
#     lat += 0.001
#     lon += 0.001
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024)
        data = data.decode("utf-8")
        lat = lat if float(data.split(",")[0]) == -1 or float(data.split(",")[0]) == 0 else float(data.split(",")[0])
        lon = lon if float(data.split(",")[1]) == -1 or float(data.split(",")[0]) == 0 else float(data.split(",")[1])
        print(lat,lon)
    except Exception as e:
        print(e)
        continue
    sendToServerAndUpdateGeoFenceStack(getTimestamp(), lat, lon)
    vehiclePosition = Point(lon, lat)
    if(flag):
        initializeGeoFenceStatusListner()
        flag = False
    print('&&',geoFenceBreachStatus)
    for i in geoFenceBreachStatus:
        if(i[2].isInsideGeoFenceWithObserver(vehiclePosition)):
            if(not geoFenceBreachStatus[geoFenceBreachStatus.index(i)][1]):
                print('send geo-fence breach notification', i[0])
                geoFenceBreachStatus[geoFenceBreachStatus.index(i)][1] = True
                ss = datetime.fromtimestamp(getTimestamp()).strftime("%I-%M %p")
                message = 'geoBreach-'+i[0]+'@'+ ss
                print(message)
                notifyServer(i[0], 'geoBreach', message)
            else:
                print('geo-fence breach but no need to send notification', i[0])
        else:
            geoFenceBreachStatus[geoFenceBreachStatus.index(i)][1] = False
            print('no breach yet')
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////")
    time.sleep(10)

