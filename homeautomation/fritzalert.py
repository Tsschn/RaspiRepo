#!/usr/bin/python

import sys
import os
import datetime
import csv
from csv import reader
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

minTemp = 5.0
maxTemp = 10.0

# letzten Eintrag aus der Datei temperaturverlauf.csv lesen
temperatureList = []

with open('temperaturverlauf.csv', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=';')
	for row in reader:
		temperatureList.append(row[2])

lastTemperature = temperatureList[len(temperatureList)-1]
print lastTemperature


msg = MIMEMultipart()
emailText = 'dummy'
doSendMail = False

# gelesene temperatur mit Minimum vergleichen
if float(lastTemperature) > float(maxTemp):
	print 'Temperatur zu hoch'
	doSendMail = True
        msg['Subject'] = "Temperatur bei Schildkroete ausserhalb des Bereiches fuer Winterruhe"
        emailText = 'Die Temperatur ist zu hoch!\nIST-Temperatur: <b>' + lastTemperature + '</b>\nMaximal erlaubte Temperatur: ' + str(round(maxTemp,2))

# gelesene temperatur mit Maximum vergleichen
if float(lastTemperature) < float(minTemp):
	print 'Temperatur zu niedrig'
	doSendMail = True
        msg['Subject'] = "Temperatur bei Schildkroete ausserhalb des Bereiches fuer Winterruhe"
        emailText = 'Die Temperatur ist zu niedrig!\nIST-Temperatur: <b>' + lastTemperature + '</b>\nMinimal erlaubte Temperatur: ' + str(round(minTemp,2))


# bei Ueberschreitung oder Unterschreitung eine Mail senden an marko.schildbach@icloud.com
if doSendMail == True:
	senderEmail = "raspberry.marko.schildbach@gmail.com"
	empfangsEmail = "marko.schildbach@icloud.com"
	msg['From'] = senderEmail
	msg['To'] = empfangsEmail

	msg.attach(MIMEText(emailText, 'html'))

	server = smtplib.SMTP("smtp.gmail.com",587) # die Server Daten
	server.starttls()
	server.login(senderEmail, "lame-astor-beware")
	text = msg.as_string()
	server.sendmail(senderEmail, empfangsEmail, text)
	server.quit()

# Protokoll schreiben
file = open('alert.log', 'a')
now = datetime.datetime.now()
logEntry = now.strftime("%Y-%m-%d") + ' - ' + now.strftime("%H:%M:%S") + ' Gemessene Temperatur: ' + lastTemperature + ' Grad. => Mail gesendet: ' + str(doSendMail)

file.write(logEntry + '\n')
file.close()

