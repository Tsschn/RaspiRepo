#!/bin/bash

BACKUP_PFAD="/media/usbstick/backup"
BACKUP_ANZAHL="100"
BACKUP_NAME="RasPi"
DIENST1="service apache2"
DIENST2="service squid"

#Stoppe Dienste vor dem Backup
sudo ${DIENST1} stop 
sudo ${DIENST2} stop 

#Backup mit Hilfe von dd erstellen und im angegebenen Pfad speichern
sudo tar -zcf ${BACKUP_PFAD}/${BACKUP_NAME}_home_$(date +%Y%m%d-%H%M%S).tar.gz /home
sudo tar -zcf ${BACKUP_PFAD}/${BACKUP_NAME}_etc_$(date +%Y%m%d-%H%M%S).tar.gz /etc
# ohne komprimierung ... sudo dd if=/dev/mmcblk0 of=${BACKUP_PFAD}/${BACKUP_NAME}-$(date +%Y%m%d-%H%M%S).img bs=1MB
sudo dd if=/dev/mmcblk0 | gzip > ${BACKUP_PFAD}/${BACKUP_NAME}_Image_$(date +%Y%m%d-%H%M%S)_mmcblk0.img.gz

# Starte Dienste nach Backup
sudo ${DIENST1} start 
sudo ${DIENST2} start
 
# Alte Sicherungen die nach X neuen Sicherungen entfernen
sudo pushd ${BACKUP_PFAD}
ls -tr ${BACKUP_PFAD}/${BACKUP_NAME}_Image* | head -n -${BACKUP_ANZAHL} | xargs rm
ls -tr ${BACKUP_PFAD}/${BACKUP_NAME}_home*  | head -n -${BACKUP_ANZAHL} | xargs rm
ls -tr ${BACKUP_PFAD}/${BACKUP_NAME}_etc*   | head -n -${BACKUP_ANZAHL} | xargs rm
popd 
