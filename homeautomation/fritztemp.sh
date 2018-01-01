#!/bin/bash
# -----------
# definitions
# -----------
FBF="http://192.168.43.1/"
USER="user"
PASS="ipass"
AIN="087610372979"
# ---------------
# fetch challenge
# ---------------
CHALLENGE=$(curl -s "${FBF}/login_sid.lua" | grep -Po '(?<=<Challenge>).*(?=</Challenge>)')
# -----
# login
# -----
MD5=$(echo -n ${CHALLENGE}"-"${PASS} | iconv -f ISO8859-1 -t UTF-16LE | md5sum -b | awk '{print substr($0,1,32)}')
RESPONSE="${CHALLENGE}-${MD5}"
SID=$(curl -i -s -k -d "response=${RESPONSE}&username=${USER}" "${FBF}" | grep -Po -m 1 '(?<=sid=)[a-f\d]+')
# -----------------
# fetch temperature
# -----------------
TEMPINT=$(curl -s ${FBF}'/webservices/homeautoswitch.lua?ain='${AIN}'&switchcmd=gettemperature&sid='${SID})
TEMPFLOAT=$(echo $TEMPINT | sed 's/\B[0-9]\{1\}\>/,&/')
# ------------------
# output temperature
# ------------------
echo $TEMPFLOAT

