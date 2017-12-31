#!/bin/bash
cat /sys/class/thermal/thermal_zone0/temp

#path to logfile
LOGFILE="/var/log/temperature_CPU.log"

#echo `date` '-' >> $LOGFILE
cat /sys/class/thermal/thermal_zone0/temp >> $LOGFILE;
































