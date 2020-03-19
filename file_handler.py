# This file inclued important method for file handling
# This is written and maintained by probhakar 19th March 2020

from utils import Point

def updateGeofenceDataBase(geoFenceData, alsoUpdateFile = True):
    # geoFenceData is defined as list of list
    #[[geoFenceID, geoFenceType, datapoints],[],]
    try:
        with open('geo_fences.txt', 'r') as f:
            data = f.read()
            f.close()
        splittedData = data.split("\n")[:-1]
        geoFenceIdAlreadyExist = []
        for i in splittedData:
            geoFenceIdAlreadyExist.append(i.split(" ")[0])
        # print(geoFenceIdAlreadyExist)
        filteredDataToUpdate = ''
        updatedGeoFenceIds = []
        for i in geoFenceData:
            if(i[0] not in geoFenceIdAlreadyExist):
                updatedGeoFenceIds.append(i[0])
                filteredDataToUpdate += i[0]+ " "+ i[1] +" "+i[2]+"\n"
            else:
                print('already exists')
        # print(filteredDataToUpdate)
        if(alsoUpdateFile):
            with open('geo_fences.txt', 'a+') as f:
                f.write(filteredDataToUpdate)
                f.close()
        return updatedGeoFenceIds
    except:
        return 'error'


def pointParser(s):
    points = []
    ls = s.split(",")
    # print(ls)
    try:
        while(len(ls) > 0):
            lat = float(ls[0])
            ls.pop(0)
            lon = float(ls[0])
            ls.pop(0)
            points.append(Point(lon, lat))

        return(points)

    except Exception as e:
        print(e)
        return 'error'


def getGeoFenceToMonitor():
    try:
        with open('geo_fences.txt', 'r') as f:
            data = f.read()
            f.close()
        splittedData = data.split("\n")[:-1]
        geoFences = []
        for i in splittedData:
            geoFences.append([i.split(" ")[0], i.split(" ")[1], pointParser(i.split(" ")[2])])
        return geoFences
    except:
        return 'error'


# updateGeofenceDataBase([['1584583122-polygon-111111111111111-3209', 'polygon', '28.498976744739682,77.05492001026869,28.495976288725284,77.05496493726969,28.493469017155235,77.05907542258501,28.495166861106586,77.06235475838184,28.499193901017073,77.06316344439983,28.50211530192782,77.06150148063898,28.502766750042966,77.05696418881416'], ['1584587634-polygon-111111111111111-1992', 'polygon', '28.4919933263656,77.04512625932693,28.488933441709978,77.04512625932693,28.487058098767854,77.04991064965725,28.489979835588308,77.05345954746008,28.494934963517085,77.05350447446108'], ['1584587681-polygon-111111111111111-8091', 'polygon', '28.49812166913808,77.07153897732496,28.497844401578494,77.0715356245637,28.497859134198304,77.07220785319805,28.49812137448643,77.0721723139286'], ['1584588052-polygon-111111111111111-5818', 'polygon', '28.51077884985534,77.05685589462519,28.506989132363067,77.0562943071127,28.507739249734378,77.06152763217688,28.503278241538055,77.06190951168537,28.503317722921345,77.0654359459877,28.507028612357697,77.06646926701069,28.51026562701899,77.06716563552618,28.51381806777799,77.0657953619957,28.51600904327743,77.06327944993973,28.51697621617791,77.0598204061389'], ['1584588092-polygon-111111111111111-6096', 'polygon', '28.51104194187962,77.0463389530778,28.511989421268982,77.05507658421993,28.509067999149458,77.05413311719894,28.509181133581414,77.05111429095268,28.504096151356766,77.05129165202379,28.503823024395476,77.04904228448868,28.508933946475327,77.0483760908246,28.50841393833609,77.0455939695239'], ['1584603825-polygon-111111111111111-8345', 'polygon', '28.521673786939818,77.02948026359081,28.517134415713763,77.02916577458382,28.51754891504808,77.0404639095068,28.522403768172826,77.04127259552479'], ['1584608847-polygon-111111111111111-4420', 'polygon', '28.466213736205408,77.03172091394663,28.450573638444585,77.0280821621418,28.452904177399628,77.02536474913359,28.463074111804975,77.02309593558311,28.457387063112037,77.01826695352793,28.469886436039307,77.02570170164108'], ['1584609248-polygon-111111111111111-8626', 'polygon', '28.494986529098835,77.07301653921604,28.497927788179393,77.07503825426102,28.495499531600043,77.07726180553436,28.4926371756228,77.07550998777151']])
# a = pointParser('28.494986529098835,77.07301653921604,28.497927788179393,77.07503825426102,28.495499531600043,77.07726180553436,28.4926371756228,77.07550998777151')
# for i in a:
#     print(i.x, i.y)