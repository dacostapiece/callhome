#!/bin/bash
exec &>>/tmp/myip_script.log

sleep 120

#Call the Python script
python /home/dacosta/CALLHOME/myip.py

sleep 10
python /home/dacosta/CALLHOME/uptime.py
