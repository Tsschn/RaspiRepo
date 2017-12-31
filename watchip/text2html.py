#!/usr/bin/python

import sys
import os
import datetime
import csv
from csv import reader
from urllib import quote

argumentCount = len(sys.argv)-1

if (argumentCount != 2):
  print "Als Argumente werden TXT-Filename und HTML-Filename erwartet."
  sys.exit(1)

#Parameter auswerten
infile = sys.argv[1]
outfile = sys.argv[2]
 

# read the data from textfile 
htmlRow1List = []

with open(infile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        htmlRow1List.append(row[0])
        #schildi ... hier evtl. mal erweitern ...

# nur die aktuellsten [n] Eintraege in der Liste behalten
maxEntriesOfList = 15
while len(htmlRow1List) > maxEntriesOfList:
	htmlRow1List.pop(0)

# open the HTML file for writing
htmlFile = open(outfile, 'w')

htmlFile.write("<html>" + '\n');
htmlFile.write("<head>" + '\n');
htmlFile.write("<title>Schildis Python text2html</title>" + '\n');
htmlFile.write("<meta http-equiv=\"expires\" content=\"0\" />" + '\n');
htmlFile.write("</head>" + '\n');
htmlFile.write("<body style = \"font-family: monospace; font-size:120%; \" >" + '\n');

for row in htmlRow1List:
	htmlLine = row
	#htmlFile.write("<p>" + "\n")
	htmlFile.write((htmlLine) + "<br/>\n")
	#htmlFile.write("</p>" + "\n")
	
htmlFile.write("</body>" + '\n');
htmlFile.write("</html>" + '\n');

htmlFile.close()

