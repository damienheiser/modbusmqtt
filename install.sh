#!/usr/bin/bash


cp ./setup/shinemonitor.service /etc/systemd/system/

systemctl enable shinemonitor.service
sudo systemctl start shinemonitor.service
