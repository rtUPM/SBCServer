#!/bin/bash

SBCServerIP=172.16.54.14
SBCSensorIP=172.16.54.15
DIR=/home/pi/

#Install packages
sudo apt-get update; sudo apt-get install -y python3-pil.imagetk

#Install pip3 modules
sudo pip3 install paho-mqtt

#Enable vnc
sudo systemctl enable vncserver-x11-serviced.service 
sudo systemctl start vncserver-x11-serviced.service

#Install SBCServer
cd $DIR; git clone https://github.com/rtUPM/SBCServer
chmod u+x SBCServer/sbc.py
chmod u+x SBCServer/scripts/*

#Change hostname
sudo sed -i 's/raspberrypi/SBCServer/' /etc/hosts
sudo sed -i 's/raspberrypi/SBCServer/' /etc/hostname

#Add sensor ip to /etc/hosts
sudo sed -i -e '$a'"${SBCSensorIP}"'  SBCSensor' /etc/hosts

#Add $DISPLAY environment variable 
echo "DISPLAY=:0.0" | sudo tee -a  /etc/environment

#Install LCD driver
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD35-show
