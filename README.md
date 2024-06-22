<b>RFE</b><br>
1) Enable hotspot if no LAN or WLAN is unavailable<br>
2) Start Webserver to receive SSID and password creds to login to neighbouring SSID

The idea is to called these scripts after a device connects to VPN Server to advertises its tun interface IP address over email.

<b>DNS_TEST.PY</b><br>
dns_test.py must run as root, therefore<br>
sudo chown root:root dns_test.py<br>
sudo chmod 700 dns_test.py<br>
<br>
<b>check permissions</b><br>
ls -al dns_test.py<br>
expected result<br>
-rwx------ 1 root root 194 mai 13 18:02 dns_test.py<br>

<b>FIXNAMESERVERS.SH</b><br>
fixnameservers.sh must run as root, therefore<br>
sudo chown root:root fixnameservers.sh<br>
sudo chmod 700 fixnameservers.sh<br>
<br>
<b>check permissions</b><br>
ls -al fixnameservers.sh<br>
expected result<br>
-rwx------ 1 root root 194 mai 13 18:02 fixnameservers.sh<br>

<b>MYIP.PY</b><br>
This script will retrieve tun0 ip address and call send_mail_my_ip_is function to send out an e-mail with this information
If tun0 has no IP address, it will send out an e-mail with error

<b>MYIP_SCRIPT.SH</b><br>
Shell script that waits 60 secs after reboot (as it's set as startup service) to call myip.py - it does also call uptime.py for script troubleshoots - it says when this .sh file was run

<b>UPTIME.PY</b><br>
myip_script.sh will call uptime.py for script troubleshoots - it says when this myip_script.sh file was run - i believe i was troubleshooting cronjob, i do not recall now

<b>OPENVPN_SCRIPT.SH</b><br>
Script run openvpn - passing creds already

<b>PASS.TXT</b><br>
OpenVPN Creds - format<br>
domain\username or username<br>
password

<b>These files are't syncing to this repo, remember creating them (creds file and grabbing your corresponding OVPN file) to follow along.</b><br>

<b>SENDMAIL.PY</b><br>
This script works as a module called by my.ip which will receive tun0 IP address for VPN and send it out as email

<b>UPDATE STATUS PANEL</b>
<b>UPDATE_STATUS_PANEL.PY</b><br>
https://dacostapiece.statuspage.io/ <br>
This script will retrieve will check if tun0 (VPN) is available and if we are able to ping a remote vpn target, so not only we ensure VPN is active, but it's also working properly.

The main goal is having a way to check wether VPN is working or not over a Web panel.

<b>Logics</b>
A) If VPN is working, check if there are existing open incidents in Atlassian Status Panel, if there's any, solve that incident, VPN is working.
B) If VPN is not working, check if there are existing open incidents in Atlassian Status Panel, if there's any, just keep it, VPN is not working.
C) If VPN is not working, check if there are existing open incidents in Atlassian Status Panel, if there's none, create one, VPN is not working.
D) If VPN is working, check if there are existing open incidents in Atlassian Status Panel, if there's none, do nothing, VPN is working.

<b>CHECK_INCIDENT_STATUS</b><br>
This script will retrieve will check if there's any existing unresolved incidents, save the JSON API response to a file and return incident id, if there's any

<b>CREATE_INCIDENT_VPN.py</b><br>
This script will create an incident, if a failure condition is met.

<b>TUNNEL_CONNECTION.py</b><br>
This script will check if tun0 is available, which means, OpenVPN is connected and try to ping a real IP address over VPN - to determine wether or not we have connection.

<b>UPDATE_INCIDENT_VPN.py</b><br>
This script will update an existing incident to solve it.

<b>UPDATE_TUN0_IPNAME.PY</b><br>
This script will retrieve tun0 IP address and update a FQDN in Cloudflare through API, so we can always reach it back the device over VPN without needing to know its current IP address, neither updating clients settings like SSH, VNC, etc...

Find your Cloudflare Zone ID<br>
Log to you Cloudflare account, access the Site/Domain you want to manipulate, account and zone id will be at the right column near bottom <br>
https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/<br>

Find your Cloudflare Record ID<br>
Create/Update the DNS Record will want to manipulate through Cloudflare dashboard<br>
"Outside site/domain panel, the place where you land just after login, go to Manage Account/Audit log<br>
Open audit logs, the DNS Record ID will be shown in the log, just click on the name far right to expand the log line<br>
https://community.cloudflare.com/t/cannot-find-record-id/326344<br>

Other references about Cloudflare settings<br>
https://developers.cloudflare.com/fundamentals/api/get-started/create-token/<br>
https://dash.cloudflare.com/profile/api-tokens<br>
https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-patch-dns-record<br>

Give permission for files to be run<br>
Example - repeat this process or call chmod +x *.py/chmod +x *.sh on the folder where scripts are stored.<br>
chmod +x /home/dacosta/CALLHOME/openvpn_script.sh<br>

<b>HOW SCRIPTS ARE CALLED?</b><br>
Some scripts are call by cronjobs, because they required often calls, some scripts are run by service, wether it runs on starts or only once and other scripts are simply called by others

<b>CRONJOBS</b><br>
To create/edit cronjobs, type crontab -e - then select your text edit (when crontab -e is called at first time), i am more familiar with nano

type sudo crontab -e to call cronjobs as root user

<b>UPDATE_TUN0_IPNAME.PY CRONJOB</b><br>
Update FQDN with current IP address at every 5min. It runs as regular raspberry user<br>
Error outputs are appended to file tmp/update_tun0_ipname.log<br>
*/5 * * * * /usr/bin/python /home/dacosta/CALLHOME/update_tun0_ipname.py >> /tmp/update_tun0_ipname.log 2>&1<br>

<b>UPDATE_STATUS_PANEL.PY</b><br>
Run script to check VPN connection and update status panel accordingly every 05 min.
*/5 * * * * /usr/bin/python /home/dacosta/CALLHOME/update_status_panel.py >> /tmp/update_status_panel.log 2>&1<br>

<b>FIXNAMESERVERS.SH</b><br>
Fix my nameserver settings in /etc/resolv.conf, that's the reason why, this script is run by root<br>
Scripts run every hour. I don't redirect errors, because the .sh script has already that, i don't know if it's required to do the same in cronjob or it'd be redudant<br>
0 * * * * /home/dacosta/CALLHOME/fixnameservers.sh<br>

<b>DNS_TEST.PY</b><br>
Checks wether DNS resolutions is working or not, then call fixnameservers.sh if it does'nt., that's the reason why, this script is run by root, because it will call another own by root file<br>
Scripts run 05 minutes. I don't redirect errors, because the .sh script has already that, i don't know if it's required to do the same in cronjob or it'd be redudant<br>
*/5 * * * * /usr/bin/python /home/dacosta/CALLHOME/dns_test.py >>/tmp/dns_test.log 2&>1<br>

<b>SERVICES</b><br>
At least in Raspberry PI, services files/settings are store in /etc/systemd/system <br>

How to add a service?<br>
sudo nano /etc/systemd/system/[service file]<br>
I am used to create files with .service extension, like ovpnscript.service<br>

<b>MANIPULATING SERVICES AFTER CREATION/UPDATE</b><br>
EXAMPLES<br>
sudo systemctl enable ovpnscript.service<br>
sudo systemctl start ovpnscript.service<br>
sudo systemctl status ovpnscript.service<br>
sudo systemctl stop ovpnscript.service<br>
sudo systemctl disable ovpnscript.service<br>

Note: If VPN is connected by this service and you stop it, it will be same as closing a running program.<br>

<b>MYIP.SERVICE</b><br>
File myip.service<br>
The service will wait 30 seconds before start, it will call myip_script.sh, it will restart on failure, but only three times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 30 seconds before trying again and it will as regular user.<br>

<b>OVPNSCRIPT.SERVICE</b><br>
File ovpnscript.service<br>
The service will start right away, it will call openvpn_script.sh, always run and it will be run as regular user.<br>

<b>UPDATEDNS.SERVICE</b><br>
File updatedns.service<br>
The service will wait 30 seconds before start, it will call update_tun0_ipname.py, it will restart on failure, but only three times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 30 seconds before trying again and it will as regular user.<br>

<b>__pycache__</b><br>
Codes are syncing to a place where codes are actually running, this folder is generated from python running

<b>VPNSTATUSPANEL.SERVICE</b><br>
File vpnstatuspanel.service<br>
The service will wait 30 seconds before start, it will call update_status_panel.py, it will restart on failure, but only three times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 30 seconds before trying again and it will as regular user. Here we set the WorkingDirectory - not sure if it's required.<br>

<b>FIXNAMESERVERS.SH</b><br>
Backup connection method - a plan b method to persist remote access to raspberry over internet, in case, vpn fails

SSH Instructions<br>
ssh -R 2222:localhost:22 -R 5901:localhost:5900 user@server

<b>bEnsure SSH Connection Remains Persistent</b><br>

To keep the SSH connection alive and reconnect automatically if it drops, you can use autossh. First, install autossh on your Raspberry Pi:

sudo apt-get install autossh
Then use autossh to create the tunnels:

autossh -M 0 -f -N -R 2222:localhost:22 -R 5901:localhost:5900 user@server
Explanation:

-M 0 disables the monitoring port feature of autossh (useful if you don't need it).
-f runs autossh in the background.
-N tells ssh not to execute a remote command.
The -R options are the same as before.
Access the Raspberry Pi from the Server

From the server, you can now access the Raspberry Pi:

For SSH:

ssh -p 2222 localhost
For VNC:
Use a VNC client to connect to localhost:5901.

<b>SSH KEYS</b><br>
Autossh requires ssh keys to be set in order to work.

<b>CREATE SERVICE</b><br>
sudo nano /etc/systemd/system/autossh.service

This service script is save under SERVICES/autossh.service in this repo

sudo systemctl enable autossh
sudo systemctl start autossh

Stopping an autossh Instance
If you started autossh manually in the background, you can find and kill the autossh process:

Find the autossh Process:
Use the ps command to find the autossh process:

<b>STOP SERVICE</b><br>
ps aux | grep autossh
Kill the autossh Process:
Identify the process ID (PID) from the output and use the kill command:

kill <PID>
If the autossh process doesn't terminate, you can forcefully kill it:

kill -9 <PID>