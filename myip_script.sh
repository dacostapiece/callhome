#!/bin/bash

# Extract paths from config.py
log_path=$(python -c "import config; print(config.myip_script_logfile)")
myip_path=$(python -c "import config; print(config.myip_script_folder_script)")

# Redirect all output to the log file
exec 2>>$log_path

# Call the Python script myip.py and check its exit code
python $myip_path
exit_code_myip=$?
if [ $exit_code_myip -ne 0 ]; then
    echo "$(date): myip.py failed with exit code $exit_code_myip" >> $log_path
    exit $exit_code_myip
fi

# If the script succeeds, exit with code 0
echo "$(date): myip.py WORKED with exit code $exit_code_myip"
exit 0
