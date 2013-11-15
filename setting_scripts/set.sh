#!/usr/bin/env bash

export SETNUM=1
export POSITION=LF
export SSID=MWRSCALE$SETNUM


export SERVERFILE=/home/pi/git/sharks/run.py
export CLIENTFILE=/home/pi/git/sharks/lcd-ui.py

case $POSITION in
LF) export IPADDR=192.168.0.1;;
LR) export IPADDR=192.168.0.2;;
RF) export IPADDR=192.168.0.3;;
RR) export IPADDR=192.168.0.4;;
esac


echo Set SSID

echo Set LF as AP and others as STA

echo Set IP Address
export NETCONFIGTMPFILE=/tmp/new.net.config
echo auto lo                                            >  NETCONFIGTMPFILE
echo iface lo inet loopback                             >> NETCONFIGTMPFILE
echo iface eth0 inet dhcp                               >> NETCONFIGTMPFILE
echo allow-hotplug wlan0                                >> NETCONFIGTMPFILE
echo iface wlan0 inet static                            >> NETCONFIGTMPFILE
echo address $IPADDR                                    >> NETCONFIGTMPFILE
echo wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf   >> NETCONFIGTMPFILE
cp NETCONFIGTMPFILE /etc/network/interfaces


echo Start Scale Server
echo Set Scale LCD
export STARTSCRIPT=/scales.sh
echo /usr/bin/env python3 $SERVERFILE $POSITION $IPADDR \& > $STARTSCRIPT
echo /usr/bin/env python2 $CLIENTFILE                   \& >> $STARTSCRIPT

echo Reboot
#reboot