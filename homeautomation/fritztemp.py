#!/usr/bin/python

import sys
import os
import datetime
import csv
from csv import reader
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
 
# read the temperature from the fritz device
process = os.popen('sudo ./fritztemp.sh')
temperature = process.read()
process.close()
 
if not temperature:
  sys.exit(1)
 
temperature = temperature.replace(',','.')
temperature = temperature.replace('\n','')
now = datetime.datetime.now()

result = now.strftime("%Y-%m-%d") + '; ' + now.strftime("%H:%M:%S") + '; ' + temperature 

print result

# write the temperature to csv file
file = open('temperaturverlauf.csv', 'a')
file.write(result + '\n')
file.close()

# read the temperature history from csv file
temperatureList = []
timeList = []

with open('temperaturverlauf.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        temperatureList.append(row[2])
	timeList.append(row[1])

# nur die aktuellsten [n] Eintraege in der Liste behalten
maxEntriesOfList = 170
while len(temperatureList) > maxEntriesOfList:
	temperatureList.pop(0)

# Bestueckung der Koordinaten fuer Diagrammdarstellung
diagrammTitle = 'Temperaturverlauf (aktuell um ' + now.strftime("%H:%M:%S") + ': ' + temperature + ' Grad)'
y = temperatureList
x = np.arange(len(temperatureList))
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(x, y, label='Temp.-Verlauf')
plt.title(diagrammTitle)
ax.legend()
#plt.show()
fig.savefig('/ftproot/temp/temperatur.png')
fig.savefig('/home/pi/webserver/temperatur.png')



