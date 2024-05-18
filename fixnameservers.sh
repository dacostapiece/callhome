#!/bin/bash
exec &>>/tmp/fixnameservers.log

sudo chattr -i /etc/resolv.conf
sudo cat /home/dacosta/CALLHOME/fixnameservers.txt > /etc/resolv.conf
cat /etc/resolv.conf >>/tmp/fixnameservers.log
