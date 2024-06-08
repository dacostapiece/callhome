#!/bin/bash
exec &>>/tmp/fixnameservers.log

# Log the current date and time
echo "" >> /tmp/fixnameservers.log
echo "updated time: $(date '+%Y-%m-%d %H:%M:%S')" >> /tmp/fixnameservers.log


sudo chattr -i /etc/resolv.conf

sudo cat /home/dacosta/CALLHOME/fixnameservers.txt > /etc/resolv.conf
cat /etc/resolv.conf >>/tmp/fixnameservers.log
