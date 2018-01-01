#!/bin/bash
#check and log if a host is reachable by ping

#CONFIGURATION

#IP of host
WATCH_IP=$1

#path to logfile
SINGLE_LOGFILE="/var/log/watchip/$WATCH_IP.log"
SINGLE_HTMLFILE="/home/pi/webserver/$WATCH_IP.html"
SUMMARY_LOGFILE="/var/log/watchip/summary.log"
SUMMARY_HTMLFILE="/home/pi/webserver/summary.html"

#duration between pings
PAUSE=30

#how many failed pings before log
TESTS=5

#SCRIPT

#initialize
MISSED=0
touch $SINGLE_LOGFILE
touch $SUMMARY_LOGFILE

while true; do
  if ! ping -c 1 -w 1 $WATCH_IP > /dev/null; then
    ((MISSED++))
  else
    if [ $MISSED -ge $TESTS ]; then
      #machine is up again
      echo `date` '- =>' $WATCH_IP >> $SINGLE_LOGFILE;
      echo `date` '- =>' $WATCH_IP >> $SUMMARY_LOGFILE;
    fi
    MISSED=0
  fi;
  if [ $MISSED -eq $TESTS ]; then
    #machine is down
    echo `date` "- <=" $WATCH_IP >> $SINGLE_LOGFILE;
    echo `date` "- <=" $WATCH_IP >> $SUMMARY_LOGFILE;
  fi
  /home/pi/scripts/watchip/text2html.py $SINGLE_LOGFILE $SINGLE_HTMLFILE 
  /home/pi/scripts/watchip/text2html.py $SUMMARY_LOGFILE $SUMMARY_HTMLFILE 
  sleep $PAUSE;
done
