<b>RFE</b><br>
1) Enable hotspot if no LAN or WLAN is unavailable (No known WLAN creds and/or range reachable)<br>
2) Handle multiple interfaces from single type - two VPNs, more than one ETH, etc...
3) Start Webserver to receive SSID and password creds to login to neighbouring SSID
4) Clean code
5) Iterate loop only on associated components IDs - VPN Checks VPNs Incidents related, SSH  Checks SSH Incidents related, and so on.

The idea is to called these scripts after a device connects to VPN Server to advertises its tun interface IP address over email.

<b>MYIP.PY</b><br>
This script will retrieve tun0 ip address from Raspberry/Remote Linux device and send out an e-mail with WIRED, WLAN and TUNNEL VPN addresses along with whole IFCONFIG in mail body message.

If tun0 has no IP address, it will send out an e-mail with error
Logs for this script are stored in /tmp/myip.py.log

Code also calls writenadreadip_tunip.py - writeip funcion to write to a file the current tun ip address. This information will be usedfor another python script.

<b>MYIP_SCRIPT.SH</b><br>
Shell script that waits 30 secs after reboot (as it's set as startup service) to call myip_script.sh and myip.py. I now know i could set up a service to call myip.py, but this is how it was setup, it'll be as is.

myip.service, myip_script.sh and myip.py has the goal to tell us by sending out an email on startup what are the available IP addresses for remote access into raspberry device.

<b>OPENVPN_SCRIPT.SH</b><br>
Script run openvpn - passing creds already
We have set up a service ovpnscript.service that calls openvpn_script.sh which is basically sending out in terminal a command line to establish a SSLVPN connection with a remote VPN Server - here called by reference purpose hub.example.com  
sudo openvpn --config /home/user/folder/file.ovpn --auth-user-pass /home/user/folder/pass.txt
You should have your own OpenVPN Server, so you can retrieve *.ovpn OpenVPN profile file as long as credentials for this VPN connection.

<b>pass.TXT</b><br>
OpenVPN Creds - format<br>
domain\username or username<br>
password

<b>*.ovpn and pass.txt are't syncing to this github repo, remember creating them (creds file and grabbing your corresponding OVPN file), store in the desired folder, prefarable callhome folder and rename openvpn_script.sh.</b><br>

<b>SENDMAIL.PY</b><br>
This script works as a module called by myip.py and updated_interfaces.py which will send out an email with WIRED, WLAN and TUNNEL VPN addresses along with whole IFCONFIG in mail body message.

<b>UPDATE STATUS PANEL</b><br>
<br>
<b>UPDATE_STATUS_PANEL.PY</b><br>
https://dacostapiece.statuspage.io/ <br>
This script will  will check if 1) tun0 (VPN) is available and if we are able to ping a remote vpn target, in our configuration it's pinging VPN Gateway private IP address, so not only we ensure VPN is active, but it's also working properly and 2) Checks if SSH Server is reachable, here in the example - server.example.com. It's basically checking if primary connection over VPN and secondary connection over SSH are working from the perspective of Raspberry/Linux local device.

The main goal is having a way to check wether VPN is working or not over a Status Web panel as well as triggering email alerts about failure incidents and restored services by Atlassian Status Panel.

You'll have to setup an account on Atlassian Status panel, it's free, to have this feature working.

<b>Logics</b>
VPN
A) If VPN is working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, if there's any, solve that incident, VPN is working.
B) If VPN is not working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, if there's any, just keep it, VPN is not working.
C) If VPN is not working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, if there's none, create an incident, VPN is not working.
D) If VPN is working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, if there's none, do nothing, VPN is working.

SSH
This script follows same logic for SSH service.

<b>CHECK_INCIDENT_STATUS</b><br>
This script will retrieve will check if there's any existing unresolved incidents for VPN in Atlassian Status Panel, save the JSON API response to a file and return component id (which service the incident is associated with) and incident id, if there's any
This script follows same logic for SSH service.

<b>CREATE_INCIDENT_VPN.py</b><br>
This script will create an incident in Atlassian Status Panel, if a failure condition is met.

<b>TUNNEL_CONNECTION.py</b><br>
This script will check if VPN or SSH is available.

<b>UPDATE_INCIDENT_VPN.py</b><br>
This script will update an existing incident to solve it in Atlassian Status Panel, if a failure no longer exists. VPN or SSH service.

<b>UPDATE_TUN0_IPNAME.PY</b><br>
This script will retrieve tun0 IP address and update a FQDN in Cloudflare through API, so we can always reach it back the device over VPN without needing to know its current IP address, neither updating clients settings like SSH, VNC, etc...

Find your Cloudflare Zone ID<br>
Log to you Cloudflare account, access the Site/Domain you want to manipulate, account and zone id will be at the right column near bottom <br>
https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/<br>

Find your Cloudflare Record ID<br>
Create/Update the DNS Record you will want to manipulate through Cloudflare API in Cloudflare's Web dashboard<br>
"Outside site/domain panel, the place where you land just after login, go to Manage Account/Audit log<br>
Open audit logs, the DNS Record ID will be shown in the log, just click on the name far right to expand the log line<br>
So if just created a DNS record or updated an existing one, audit logs will show them right in top of audit logs, you can expand that information to retrieve DNS Record ID.
https://community.cloudflare.com/t/cannot-find-record-id/326344<br>

Other references about Cloudflare settings<br>
https://developers.cloudflare.com/fundamentals/api/get-started/create-token/<br>
https://dash.cloudflare.com/profile/api-tokens<br>
https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-patch-dns-record<br>

Give permission for files to be run<br>
Example - repeat this process or call chmod +x *.py/chmod +x *.sh on the folder where scripts are stored.<br>
chmod +x /home/dacosta/CALLHOME/openvpn_script.sh<br>

<b>HOW SCRIPTS ARE CALLED?</b><br>
Some scripts are call by cronjobs, because they required recurring calls, some scripts are run by service, it runs on device startup or only once and other scripts are simply called by others scripts in chain.

<b>CRONJOBS</b><br>
To create/edit cronjobs, type crontab -e - then select your text editor (when crontab -e is called at first time), i am more familiar with nano

type sudo crontab -e to call cronjobs as root user (not required for our current scripts)

<b>UPDATE_TUN0_IPNAME.PY CRONJOB</b><br>
Update FQDN with current IP address at every 5min. It runs as regular raspberry user<br>
Error outputs are appended to file tmp/update_tun0_ipname.log<br>
*/5 * * * * /usr/bin/python /home/dacosta/CALLHOME/update_tun0_ipname.py >> /tmp/update_tun0_ipname.log 2>&1<br>

<b>UPDATE_STATUS_PANEL.PY</b><br>
Run script to check VPN connection and update status panel accordingly every 05 min.
*/5 * * * * /usr/bin/python /home/dacosta/CALLHOME/update_status_panel.py >> /tmp/update_status_panel.log 2>&1<br>
Troubleshoot or check cronjob run status in here /tmp/update_status_panel.log
Rememeber to update this with your local path /home/user/folder/update_status_panel.py
You can use "which python" to see where is the full path for python binary
For me is /usr/bin/python

<b>SERVICES</b><br>
At least in Raspberry PI, services files/settings are store in /etc/systemd/system <br>

How to add a service?<br>
sudo nano /etc/systemd/system/[service file]<br>
I am used to create files with .service extension, like ovpnscript.service<br>

<b>MANIPULATING SERVICES AFTER CREATION/UPDATE</b><br>
EXAMPLES<br>
sudo systemctl enable ovpnscript.service<br> //enable service after file creation
sudo systemctl start ovpnscript.service<br> //start service
sudo systemctl status ovpnscript.service<br> //check service status
sudo systemctl stop ovpnscript.service<br> //stop service
sudo systemctl disable ovpnscript.service<br> //disable service
sudo systemctl daemon-reload<br> //when changes are applied to service file, it'll be requested to update is daemon

Note: If VPN is connected by this service and you stop it, it will be same as closing a running program.<br>

<b>MYIP.SERVICE</b><br>
File myip.service<br>
The service will wait 30 seconds before start, it will call myip_script.sh, it will restart on failure, but only six times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 60 seconds before trying again and it will as run regular user.<br>

<b>OVPNSCRIPT.SERVICE</b><br>
File ovpnscript.service<br>
The service will start right away, it will call openvpn_script.sh, always run and it will be run as regular user.<br>

<b>UPDATEDNS.SERVICE</b><br>
File updatedns.service<br>
The service will wait 30 seconds before start, it will call update_tun0_ipname.py, it will restart on failure, but only three times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 30 seconds before trying again and it will run as regular user.<br>

<b>__pycache__</b><br>
Codes are syncing to a place where codes are actually running, this folder is generated from python running. This folder is set to not sync with Github.

<b>VPNSTATUSPANEL.SERVICE</b><br>
File vpnstatuspanel.service<br>
The service will wait 30 seconds before start, it will call update_status_panel.py, it will restart on failure, but only three times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 30 seconds before trying again and it will run as regular user. Here we set the WorkingDirectory - not sure if it's required.<br>

Backup connection method - a plan B method to persist remote access to raspberry over internet, in case, vpn fails

<b>SSH KEYS</b><br>
Autossh requires ssh keys to be set in order to work.

<b>CREATE SERVICE</b><br>
sudo nano /etc/systemd/system/autossh.service

This service script is save under SERVICES/autossh.service in this repo

sudo systemctl enable autossh
sudo systemctl start autossh

Stopping an autossh instance manually
1) sudo systemctl stop  autossh
2) killall autossh

<h1>DRAFT</h1><br>
<b>SAMPLE SIMPLE CURL</b><br>
<h1>So you can test API communication with Atlassian</h1><br>
```bash
curl https://api.statuspage.io/v1/pages/{page_id}/incidents \
  -H "Authorization: OAuth {api_token}" \
  -X POST \
  -d "incident[name]=Teste Component" \
  -d "incident[status]=investigating" \
  -d "incident[body]=Testando componentes" \
  -d "incident[component_ids][]={component id}" \
  -d "incident[component_ids][]={component id2}" \
  -d "incident[components][{component id}]=major_outage" \
  -d "incident[components][{component id}2]=major_outage"
```

```bash
