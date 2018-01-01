#!/bin/bash
cd /home/pi/scripts/speedtest/
speedtest --csv --csv-delimiter=";" >> speedtest.log
python /home/pi/scripts/speedtest/speedtest.py
