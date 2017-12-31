#!/usr/bin/python
# ermittelt die CPU-Temperatur aus einem logfile und erzeugt ein Diagramm
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
process = os.popen('sudo ./temperature.sh')
temperature = process.read()
process.close()
 
if not temperature:
  sys.exit(1)
 
temperature = temperature.replace(',','.')
temperature = temperature.replace('\n','')
temperature = str(round(float(temperature) / 1000, 1))
now = datetime.datetime.now()

result = now.strftime("%Y-%m-%d") + '; ' + now.strftime("%H:%M:%S") + '; ' + temperature 

print result

# write the temperature to csv file
file = open('cpu_temperature.csv', 'a')
file.write(result + '\n')
file.close()

# read the temperature history from csv file
temperatureList = []
timeList = []

with open('cpu_temperature.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        temperatureList.append(row[2])
	timeList.append(row[1])

# nur die aktuellsten [n] Eintraege in der Liste behalten
maxEntriesOfList = 300
while len(temperatureList) > maxEntriesOfList:
	temperatureList.pop(0)

# Bestueckung der Koordinaten fuer Diagrammdarstellung
diagrammTitle = 'CPU-Core Temperaturverlauf (aktuell um ' + now.strftime("%H:%M:%S") + ': ' + temperature + ' Grad)'
y = temperatureList
x = np.arange(len(temperatureList))
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(x, y, label='Temp.-Verlauf')
plt.title(diagrammTitle)
ax.legend()
#plt.show()
fig.savefig('/ftproot/temp/cpu_temperatur.png')
fig.savefig('/home/pi/webserver/cpu_temperatur.png')

