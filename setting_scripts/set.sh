#!/usr/bin/env bash
###############################################################################
#
###############################################################################

export SETNUM=2
export POSITION=RF
export SSID=MWRSCALE$SETNUM

export SERVERFILE=/home/pi/git/sharks/run.py
export CLIENTFILE=/home/pi/git/sharks/lcdui.py
export MSGFILE=/home/pi/git/sharks/set-red-message.py

export STARTSCRIPT=/scales.sh
echo "#Sharks starup" > $STARTSCRIPT

case $POSITION in
LF) export IPADDR=192.168.0.1;;
LR) export IPADDR=192.168.0.2;;
RF) export IPADDR=192.168.0.3;;
RR) export IPADDR=192.168.0.4;;
esac

echo Set Scale Label
export HEADERFILE="/etc/sharks.header"
echo SET$SETNUM\:$POSITION > $HEADERFILE


echo Set SSID
export HOSTAPDTMPFILE="/tmp/hostapd.conf"
echo interface=wlan0               >   $HOSTAPDTMPFILE 
echo driver=rtl871xdrv             >>  $HOSTAPDTMPFILE
echo country_code=NZ               >>  $HOSTAPDTMPFILE
echo ctrl_interface=wlan0          >>  $HOSTAPDTMPFILE
echo ctrl_interface_group=0        >>  $HOSTAPDTMPFILE
echo ssid=$SSID                    >>  $HOSTAPDTMPFILE
echo hw_mode=b                     >>  $HOSTAPDTMPFILE
echo channel=1                     >>  $HOSTAPDTMPFILE
echo wpa=3                         >>  $HOSTAPDTMPFILE
echo wpa_passphrase=5057501807     >>  $HOSTAPDTMPFILE
echo wpa_key_mgmt=WPA-PSK          >>  $HOSTAPDTMPFILE
echo wpa_pairwise=TKIP             >>  $HOSTAPDTMPFILE
echo rsn_pairwise=CCMP             >>  $HOSTAPDTMPFILE
echo beacon_int=100                >>  $HOSTAPDTMPFILE
echo auth_algs=3                   >>  $HOSTAPDTMPFILE
echo macaddr_acl=0                 >>  $HOSTAPDTMPFILE
echo wmm_enabled=1                 >>  $HOSTAPDTMPFILE
echo eap_reauth_period=360000000   >>  $HOSTAPDTMPFILE

export WPACLIENTFILE="/etc/wpa-client.conf"
echo "ctrl_interface=/var/run/wpa_supplicant" >  $WPACLIENTFILE
echo "network={"                              >> $WPACLIENTFILE
echo "   ssid=\"$SSID\""                      >> $WPACLIENTFILE
echo "   key_mgmt=WPA-PSK"                    >> $WPACLIENTFILE
echo "   psk=\"5057501807\""                  >> $WPACLIENTFILE
echo "}"                                      >> $WPACLIENTFILE

echo Set LF as AP and others as STA

if [ "$POSITION" = "LF" ]
    then
    echo AP;
    # turn AP on
    cp $HOSTAPDTMPFILE /etc/hostapd/hostapd.conf
    else
    echo STA ;
    # turn AP off
    rm /etc/hostapd/hostapd.conf
    # turn sta on
    echo /sbin/iwconfig wlan0 essid $SSID                                                    >>  $STARTSCRIPT
    echo /sbin/ifconfig wlan0 $IPADDR                                                        >>  $STARTSCRIPT
    echo /usr/bin/killall wpa_supplicant                                                     >>  $STARTSCRIPT
    echo /sbin/wpa_supplicant -c$WPACLIENTFILE -iwlan0 -Dwext 2\> /var/log/wpa-client.log \& >>  $STARTSCRIPT

fi


echo Set IP Address
export NETCONFIGTMPFILE="/tmp/new.net.config"
echo auto lo                                            >  $NETCONFIGTMPFILE
echo iface lo inet loopback                             >> $NETCONFIGTMPFILE
echo iface eth0 inet dhcp                               >> $NETCONFIGTMPFILE
echo allow-hotplug wlan0                                >> $NETCONFIGTMPFILE
echo iface wlan0 inet static                            >> $NETCONFIGTMPFILE
echo address $IPADDR                                    >> $NETCONFIGTMPFILE
echo wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf   >> $NETCONFIGTMPFILE
cp $NETCONFIGTMPFILE /etc/network/interfaces


echo Start Scale Server
echo Set Scale LCD
echo /usr/bin/python2 $CLIENTFILE           $IPADDR 2\> /var/log/sharks-lcd.log    \& >>  $STARTSCRIPT
echo /usr/bin/python3 $SERVERFILE $POSITION $IPADDR 2\> /var/log/sharks-server.log \& >>  $STARTSCRIPT
cp $STARTSCRIPT /etc/rc.local

echo Reboot
killall python2
killall python3
/usr/bin/python2 $MSGFILE "Rebooting..."; 
reboot
/usr/bin/python2 $MSGFILE "Reboot Failed\nPower Cycle"; 
