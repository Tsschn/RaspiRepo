#!/usr/bin/python
# wertet speedtest.log aus und erzeugt ein Diagramm
import sys
import os
import datetime
import csv
from csv import reader
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
 
# read the temperature history from csv file
pingList = []
uploadList = []
downloadList = []
timeList = []
now = datetime.datetime.now()

with open('speedtest.log', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
    	try:
		pingList.append(str(round(float(row[5]) / 1000000, 1)))
        	downloadList.append(str(round(float(row[6]) / 1000000, 1)))
        	uploadList.append(str(round(float(row[7]) / 200000, 1)))
		parsedTime = datetime.datetime.strptime(str(row[3]),"%Y-%m-%dT%H:%M:%S.%f")
        	formattedTime = "{:d}:{:02d}".format(parsedTime.hour, parsedTime.minute)
        	timeList.append(formattedTime)
		#print formattedTime
	except (IndexError, ValueError):
		print "===> Ungueltige Werte eingelesen: " + str(row)
		continue

# nur die aktuellsten [n] Eintraege in der Liste behalten
maxEntriesOfList = 48
print "Berechnung der letzten " + str(maxEntriesOfList) + " Messungen."
while len(pingList) > maxEntriesOfList:
	pingList.pop(0)
	uploadList.pop(0)
	downloadList.pop(0)
	timeList.pop(0)

# Bestueckung der Koordinaten fuer Diagrammdarstellung
matplotlib.rcParams.update({'font.size': 6})

lastDownload = downloadList[len(downloadList)-1]
diagrammTitle = 'Speedtest (aktuell um ' + now.strftime("%H:%M:%S") + ': ' + lastDownload + ' MBit/s)'
fig = plt.figure()
ax = plt.subplot(111)

plt.xticks(np.arange(len(timeList)), timeList)
ax.plot(np.arange(len(downloadList)), downloadList, label='Download MBit/s')
ax.plot(np.arange(len(uploadList)), uploadList, label='Upload MBit/s * 5')

plt.xticks(rotation=90)
plt.title(diagrammTitle)
ax.legend()

fig.savefig('/ftproot/temp/speedtest.png')
fig.savefig('/home/pi/webserver/speedtest.png')

