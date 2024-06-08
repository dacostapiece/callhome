#!/bin/bash
exec &>>/tmp/myip_script.log

#Call the Python script
python /home/dacosta/CALLHOME/myip.py
