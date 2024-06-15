#!/bin/bash

# Redirect all output to the log file
exec &>>/tmp/myip_script.log

# Call the Python script myip.py and check its exit code
python /home/dacosta/CALLHOME/myip.py
exit_code_myip=$?
if [ $exit_code_myip -ne 0 ]; then
    echo "$(date): myip.py failed with exit code $exit_code_myip" >> /tmp/myip_script.log
    exit $exit_code_myip
fi

# If the script succeeds, exit with code 0
exit 0
