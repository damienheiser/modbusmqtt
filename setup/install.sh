#!/usr/bin/sh
SERVICE=modbusmqtt

systemctl stop $SERVICE.service

CONF_DIR = /etc/$SERVICE
MAPS_DIR = $CONF_DIR/devices
mkdir -p $MAPS_DIR

FILE=$CONF_DIR/$SERVICE.conf
if test -f "$FILE"; then
    echo "$FILE exists, skipping"
else
    cp ./setup/settings.conf $FILE
fi

sed  's|{path}|'${PWD}'|' ./setup/$SERVICE.service > /etc/systemd/system/$SERVICE.service

systemctl enable $SERVICE.service
systemctl start $SERVICE.service