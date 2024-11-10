#!/bin/bash

# Extract paths from config.py
logfile_path=$(python -c "import config; print(config.openvpn_logfile)")
profile_path=$(python -c "import config; print(config.openvpn_script_profile)")
auth_path=$(python -c "import config; print(config.openvpn_script_auth)")

exec &>>$logfile_path
sudo openvpn --config $profile_path --auth-user-pass $auth_path