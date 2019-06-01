"""
Solution for project.
Do all the various calculations and operations on the readings.
Author: Rahul Chakraborty
"""

import math

def convertLatLong(lat, long):
    '''
    Convert latitude and longitude into degrees
    :param lat: Latitude
    :param long:Longitude
    :return: converted latitude and longitude respectively
    '''
    convLat = lat // 100 + (lat % 100) / 60
    convLong = long // 100 + (long % 100) / 60
    return convLat, convLong

def computeMinCostFun(readingsPerFile):
    '''
    Calculate minimum cost function for each trip
    param:
    :param readingsPerFile:
    :return: minimum Cost function
    '''
    maxVelocity = 0
    for eachReading in readingsPerFile:
        speedMph = float(eachReading[7]) * 1.15078 # get speed in mph
        if(speedMph>maxVelocity):
            maxVelocity = speedMph

    # calc largest time in minutes
    lastTimeGMT = float(readingsPerFile[len(readingsPerFile)-1][1])
    lastTimeHour = lastTimeGMT//1000
    lastTimeMin = (lastTimeGMT-lastTimeHour*1000)//100

    # calc smallest time in minutes
    firstTimeGMT = float(readingsPerFile[0][1])
    firstTimeHour = firstTimeGMT // 1000
    firstTimeMin = (firstTimeGMT - firstTimeHour * 1000) // 100

    travelTime = lastTimeMin-firstTimeMin
    costFunc = (travelTime/30)+(1/2)*(maxVelocity/60)

    return costFunc


def locateStopSignsAndGenerateKML(allReadings):
    '''
    Identify stops in the readings and generate KML file.
    KML file contains all stops marked with red placemarks
    :param readingsList: Cleaned RMC readings
    :return:
    '''
    longForStopsList = [] #Store all longitudes for stops
    latForStopsList = [] #Store all latitudes for stops
    for eachReadingsList in allReadings:
        for eachReading in eachReadingsList:
            #Take readings which have speeds less than 5 mph
            speedMph = float(eachReading[7]) * 1.15078
            print(speedMph)
            if(speedMph<0.1): # stop is when the car does not have a speed
                lat = float(eachReading[3])
                long = float(eachReading[5])
                convLat, convLong = convertLatLong(lat, long) #Convert latitude and longitude to angles
                if (eachReading[4] == 'S'):
                    convLat = -convLat
                if (eachReading[6] == 'W'):
                    convLong = -convLong
                longForStopsList.append(convLong)
                latForStopsList.append(convLat)

    latForStopsList = [latForStopsList for longForStopsList, latForStopsList
                          in sorted(zip(longForStopsList, latForStopsList))]  # sort latitudes as per ascending order of longitudes
    longForStopsList.sort()
    f = open('stops.kml', "w+")
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    f.write('\n<kml xmlns="http://www.opengis.net/kml/2.2">')
    f.write('\n<Document>')
    for i in range(len(longForStopsList)):
        f.write('\n<Placemark>')
        f.write('\n<description>Red PIN for A Stop</description>')
        f.write('\n<Style id = "normalPlacemark">')
        f.write('\n<IconStyle>')
        f.write('\n<color>ff0000ff</color>')
        f.write('\n<Icon>')
        f.write('\n<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>')
        f.write('\n</Icon>')
        f.write('\n</IconStyle>')
        f.write('\n</Style>')
        f.write('\n<Point>')
        f.write('\n<coordinates>')
        f.write(str(longForStopsList[i])+','+str(latForStopsList[i]))
        f.write('</coordinates>')
        f.write('\n</Point>')
        f.write('\n</Placemark>')

    f.write('\n</Document>')
    f.write('\n</kml>')


def locateLeftTurnAndGenerateKML(allReadings):
    '''
    :param readingsList: Cleaned RMC readings
    :return:
    '''
    longForLeftList = []  # Store all longitudes for left turns
    latForLeftList = []  # Store all latitudes for left turns
    for eachReadingsList in allReadings:
        for i in range(len(eachReadingsList)):
            # Take readings which have speeds less than 5 mph
            if(i!=0):
                if (float(eachReadingsList[i][5])-float(eachReadingsList[i-1][5])>=65 and
                    float(eachReadingsList[i][5]) - float(eachReadingsList[i - 1][5]) <= 115):  # stop is when the car does not have a speed
                    lat = float(eachReadingsList[i][3])
                    long = float(eachReadingsList[i][5])
                    convLat, convLong = convertLatLong(lat, long)  # Convert latitude and longitude to angles
                    if (eachReading[4] == 'S'):
                        convLat = -convLat
                    if (eachReading[6] == 'W'):
                        convLong = -convLong
                    longForLeftList.append(convLong)
                    latForLeftList.append(convLat)

    latForLeftList = [latForLeftList for longForLeftList, latForLeftList in sorted(zip(longForLeftList, latForLeftList))]  # sort latitudes as per ascending order of longitudes
    longForLeftList.sort()
    f = open('left_turns.kml', "w+")
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    f.write('\n<kml xmlns="http://www.opengis.net/kml/2.2">')
    f.write('\n<Document>')
    for i in range(len(longForLeftList)):
        f.write('\n<Placemark>')
        f.write('\n<description>Default Pin is Yellow</description>')
        f.write('\n<Style id = "normalPlacemark">')
        f.write('\n<IconStyle>')
        f.write('\n<color>Af00ffff</color>')
        f.write('\n<Icon>')
        f.write('\n<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>')
        f.write('\n</Icon>')
        f.write('\n</IconStyle>')
        f.write('\n</Style>')
        f.write('\n<Point>')
        f.write('\n<coordinates>')
        f.write(str(longForLeftList[i]) + ',' + str(latForLeftList[i]))
        f.write('</coordinates>')
        f.write('\n</Point>')
        f.write('\n</Placemark>')

    f.write('\n</Document>')
    f.write('\n</kml>')


def convertValueGenerateKML(readingsList, count):
    '''
    Generate KML file for each of the routes using a cleaned reading list.
    :param readingsList: Cleaned RMC readings
    :return:
    '''
    filename = "track"+str(count)+".kml"
    f = open(filename, "w+")
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    f.write('\n<kml xmlns="http://www.opengis.net/kml/2.2">')
    f.write('\n<Document>')
    f.write('\n<Style id="yellowPoly">')
    f.write('\n<LineStyle>')
    f.write('\n\<color>Af00ffff</color>')
    f.write('\n<width>6</width>')
    f.write('\n</LineStyle>')
    f.write('\n<PolyStyle>')
    f.write('\n<color>7f00ff00</color>')
    f.write('\n</PolyStyle>')
    f.write('\n</Style>')
    f.write('\n<Placemark>') #<styleUrl>#yellowPoly</styleUrl>')
    f.write('\n<LineString>')
    f.write('\n<Description>')
    f.write('\n</Description>')
    f.write('\n<extrude>1</extrude>')
    f.write('\n<tesselate>1</tesselate>')
    f.write('\n<coordinates>')
    for eachReading in readingsList:
        lat = float(eachReading[3])
        long = float(eachReading[5])
        convLat, convLong = convertLatLong(lat, long)
        if (eachReading[4] == 'S'):
            convLat = -convLat
        if (eachReading[6] == 'W'):
            convLong = -convLong
        f.write('\n'+str(convLong))
        f.write(',')
        f.write(str(convLat))

    f.write('\n</coordinates>')
    f.write('\n</LineString>')
    f.write('\n</Placemark>')
    f.write('\n</Document>')
    f.write('\n</kml>')

def removeRedundantandErroneousData(impReadingsList):
    '''
    Remove all redundant and erroneous data from the important readings list
    :param: impReadingsList - Readings before removal of redundant stop readings
    :return: updatedReadingsList - Readings after removal of redundant stop readings
    '''
    firstStopReadingFound = False #Check first stop reading - car is stationary or speed is 0.00 knots
    updatedReadingsList = [] #Updated reading this list that only contains non-redudant readings
    for i in range(len(impReadingsList)):
        if(float(impReadingsList[i][7])<=2.00):
            if(firstStopReadingFound):
                # check if car is in the exact same position(same latitude and longitude as previous reading) and it does not move
                if float(impReadingsList[i][3])==float(impReadingsList[i-1][3]) and float(impReadingsList[i][5])==float(impReadingsList[i-1][5]):
                    print(impReadingsList[i][3],impReadingsList[i][5],impReadingsList[i][7])
                    impReadingsList[i].append(False) # This means car stops and stays in the same location - discard these readings
                else:
                    firstStopReadingFound=False
                    impReadingsList[i].append(True)

            else:
                firstStopReadingFound = True # First time car stops
                impReadingsList[i].append(True) # Keep these readings

        else:
            if(firstStopReadingFound):
                firstStopReadingFound = False  # Make sure this is always False when True

            impReadingsList[i].append(True) # Keep these readings


    '''for i in range(len(impReadingsList)):
        # check if car is in the exact same position(same latitude and longitude as previous reading) and it does not move
        if float(impReadingsList[i][3]) == float(impReadingsList[i - 1][3]) and float(impReadingsList[i][5]) == float(impReadingsList[i - 1][5]) and i!=0:
            impReadingsList[i].append(False)  # This means car stops and stays in the same location - discard these readings
        else:
            impReadingsList[i].append(True)'''


    for impReadings in impReadingsList:
        if(impReadings[len(impReadings)-1] is True):
            updatedReadingsList.append(impReadings[0:len(impReadings)-1]) # No need to keep the last boolean value

    return updatedReadingsList



if __name__ == '__main__':
    # store all the file names of all readings
    filenames = ['ZI8G_ERF_2018_08_16_1428.txt','ZI8H_HJC_2018_08_17_1745.txt','ZI8J_GKX_2018_08_19_1646.txt',
                 'ZI8K_EV7_2018_08_20_1500.txt','ZI8N_DG8_2018_08_23_1316.txt','ZIAA_CTU_2018_10_10_1255.txt',
                 'ZIAC_CO0_2018_10_12_1250.txt']

    rmcReadingsList = [] # store all rmc readings of all the files together

    for filename in filenames:
        rmcReadingPerFile = []
        with open(filename) as f:
            for line in f:
                if(line.split(',')[0]=="$GPRMC"):
                    rmcReadingPerFile.append(line)

        rmcReadingsList.append(rmcReadingPerFile)

    eachReadingSplit = [] # split all the individual fields in the RMC and convert them into a values of a list
    updatedReadingsList = [] # used to store all the readings as a list of list fields

    for rmcReadingPerFile in rmcReadingsList:
        updatedReadingsPerFile = []
        for eachReading in rmcReadingPerFile:
            index = 0 #keep track of index while tying to append all readings into impReadingsList
            eachReadingSplit = eachReading.split(',')
            #print(len(eachReadingSplit))
            if(eachReadingSplit[3]!='' and len(eachReadingSplit)<=13): # discard all readings with no longtiude and usually large parameters
                updatedReadingsPerFile.append(eachReadingSplit)
                #print(eachReadingSplit, len(eachReadingSplit))
        updatedReadingsList.append(updatedReadingsPerFile)

    '''
    Position of each data in the reading in each eachReadingSplit[] list is:
    0 - Reading type ($GPRMC)
    1 - Time in GMT or UTC
    2 - A
    3 - Latitude 
    4 - N for North 
    5 - Longitude
    6 - W for west 
    7 - Speed in Knots
    8 - Tracking angle
    9 - Date in DDMMYY format
    '''

    newUpdateReadingsList = []
    for updatedReadingsPerFile in updatedReadingsList:
        newUpdateReadingsList.append(removeRedundantandErroneousData(updatedReadingsPerFile))

    # Generate KML files for all readings for each of the 7 files
    count = 1
    for updatedReadingsPerFile in newUpdateReadingsList:
        convertValueGenerateKML(updatedReadingsPerFile, count)
        count+=1

    #Generate KML for left turns
    locateLeftTurnAndGenerateKML(newUpdateReadingsList)
    # Generate KML for stop signs
    locateStopSignsAndGenerateKML(newUpdateReadingsList)

    minCostFunc = math.inf
    costFuncPerFile = math.inf
    index = -1

    # Calculate path with best function
    for i in range(len(newUpdateReadingsList)):
        costFuncPerFile = computeMinCostFun(newUpdateReadingsList[i])
        if(costFuncPerFile<minCostFunc):
            minCostFunc = costFuncPerFile
            index = i

    print("Best cost function is file:",filenames[index])

