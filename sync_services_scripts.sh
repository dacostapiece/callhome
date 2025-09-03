#!/bin/bash

# Extract paths from config.py
myip_path=$(python -c "import config; print(config.myip_service_path)")
ovpnscript_path=$(python -c "import config; print(config.ovpnscript_service_path)")
updatedns_path=$(python -c "import config; print(config.updatedns_service_path)")
vpnstatuspanel_path=$(python -c "import config; print(config.vpnstatuspanel_service_path)")
autossh_path=$(python -c "import config; print(config.autossh_service_path)")

cat /etc/systemd/system/myip.service >$myip_path
cat /etc/systemd/system/ovpnscript.service >$ovpnscript_path
cat /etc/systemd/system/updatedns.service >$updatedns_path
cat /etc/systemd/system/vpnstatuspanel.service >$vpnstatuspanel_path
cat /etc/systemd/system/autossh.service >$autossh_path