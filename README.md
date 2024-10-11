<b>RFE</b><br>
1) Enable hotspot if no LAN or WLAN is unavailable (No known WLAN creds and/or range reachable)<br>
2) Handle multiple interfaces from single type - two VPNs, more than one ETH, etc...
3) Start Webserver to receive SSID and password creds to login to neighbouring SSID
4) Clean code
5) Iterate loop only on associated components IDs - VPN Checks VPNs Incidents related, SSH  Checks SSH Incidents related, and so on.

The idea is to called these scripts after a device connects to VPN Server to advertises its tun interface IP address over email.

<b>AUTOSSH.PY</b><br>
This is script is responsible to start and maintain an SSH connection to an outside server here called server.example.com<br>
Through this connection Raspberry/Linux local device will connect to and exposed its own SSH service (terminal access) and VNC (graphical access)<br>
So it gives a backup/secondary way to reach Raspberry device and network it's connected to even in incident where VPN server (primary connection) fails<br>
1) It starts the autossh process<br>
2) It resolves DNS if the server address is a fully qualified domain name (FQDN)<br>
3) Verifies the externalSSH server is reachable<br>
4) If the SSH server is reachable - it starts SSH Agent and Add SSH key, if not call restart_ssh and then exit error<br>
Restart SSH will kill existing autossh processes (it may be running, but real connection is not established)<br>
and reinitiate the autossh process again<br>
5) Run autossh command<br>
6) Sends over SSH connection a calling<br>
Example<br>
ssh {user}@{ssh_server} \"echo '{ip_address}' > {remote_path}<br>
<b>192.168.0.10</b> is an example tunnel ip address<br>
```bash
ssh user@server.example.com \"echo '192.168.0.10' > /home/user/folder/current_rasp_ip.txt
```

7) Checks if SSH tunnel is established, if not, exit with error
8) If not any exit error, checks autossh existing process<br>

The goal with this command is recover current Raspberry device IP address for Tunnel VPN and a create a file in SSH Server, <br>another script will read this file in the SSH Server and knows which IP address to ping it back to test "Callback VPN" connection from SSH Server to Raspberry itself<br>
Later in this project we've realized we could simply tell SSH Server to ping <b>raspberry.example.com</b> which is an FQDN that's often update from<br> Raspberry to Cloudflare API to expose Raspberry's VPN IP address, but for the time being, we won't update this script logics.<br>

This scripts runs on startup with autossh.service<br>
And runs every 05min as cronjob<br>
Logs for this script are stored in /tmp/autossh_script.log

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
```bash
sudo openvpn --config /home/user/folder/file.ovpn --auth-user-pass /home/user/folder/pass.txt
```

You should have your own OpenVPN Server, so you can retrieve *.ovpn OpenVPN profile file as long as credentials for this VPN connection.

<b>PASS.TXT</b><br>
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
This script will  will check if <br>
1) tun0 (VPN) is available and if we are able to ping a remote vpn target, in our configuration it's pinging VPN Gateway private IP address, so not only we ensure VPN is active, but it's also working properly and <br>
2) Checks if SSH Server is reachable, here in the example - server.example.com. <br>
It's basically checking if primary connection over VPN and secondary connection over SSH are working from the perspective of Raspberry/Linux local device.

The main goal is having a way to check wether VPN is working or not over a Status Web panel as well as triggering email alerts about failure incidents and restored services by Atlassian Status Panel.

You'll have to setup an account on Atlassian Status panel, it's free, to have this feature working.

<b>Logics</b><br>
VPN<br>
A) If VPN is working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, if there's any, solve that incident, VPN is working.<br>
B) If VPN is not working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, if there's any, just keep it, VPN is not working.<br>
C) If VPN is not working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, if there's none, create an incident, VPN is not working.<br>
D) If VPN is working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, if there's none, do nothing, VPN is working.<br>

SSH<br>
This script follows same logic for SSH service.<br>

This scripts runs on startup with vpnstatuspanel.service<br>
And runs every 05min as cronjob<br>

<b>CHECK_INCIDENT_STATUS.PY</b><br>
This script will retrieve will check if there's any existing unresolved incidents for VPN in Atlassian Status Panel, save the JSON API response to a file and return component id (which service the incident is associated with) and incident id, if there's any
This script follows same logic for SSH service.

<b>CREATE_INCIDENT_VPN.py</b><br>
This script will create an incident in Atlassian Status Panel, if a failure condition is met.

<b>TUNNEL_CONNECTION.py</b><br>
This script will check if VPN or SSH is available.

<b>UPDATE_INCIDENT_VPN.py</b><br>
This script will update an existing incident to solve it in Atlassian Status Panel, if a failure no longer exists. VPN or SSH service.

<b>UPDATE_TUN0_IPNAME.PY</b><br>
This script will retrieve tun0 IP address and update a FQDN in Cloudflare through API, so we can always reach it back the device over VPN without<br>
needing to know its current IP address, neither updating clients settings like SSH, VNC, etc...<br>
In this example is <b>raspberry.example.com</b><br>
This scripts runs on startup with updatedns.service<br>
And runs every 05min as cronjob<br>

Cloudflare Nameserver and API services for free are compatible with this project, you can just create an account and move or register an FQDN<br> domain and associate to Cloudflare nameservers before moving on. Do not enable Cloudflare DNS proxy for DNS records that will be used within this project. <br>

Create/Find your Cloudflare API Token<br>
1) Log to your Cloudflare account<br>
2) Manage Account<br>
3) Acocunt API Tokens<br>
4) Create API Token with Edit DNS Zone permissions<br>
https://developers.cloudflare.com/fundamentals/api/get-started/create-token/<br>

Find your Cloudflare Zone ID<br>
Log to you Cloudflare account, access the Site/Domain you want to manipulate, account and zone id will be at the right column near bottom <br>
https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/<br>

Find your Cloudflare DNS Record ID<br>
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
```bash
chmod +x /home/dacosta/CALLHOME/openvpn_script.sh
```

<b>HOW SCRIPTS ARE CALLED?</b><br>
Some scripts are call by cronjobs, because they required recurring calls, some scripts are run by service, it runs on device startup or only once and other scripts are simply called by others scripts in chain.

<b>CRONJOBS</b><br>
To create/edit cronjobs, type 
```bash
crontab -e
```
 - then select your text editor (when crontab -e is called at first time), i am more familiar with nano

type 
```bash
sudo crontab -e
```

to call cronjobs as root user (not required for our current scripts)

<b>UPDATE_TUN0_IPNAME.PY CRONJOB</b><br>
Update FQDN with current IP address at every 5min. It runs as regular raspberry user<br>
Error outputs are appended to file tmp/update_tun0_ipname.log<br>
```bash
*/5 * * * * /usr/bin/python /home/dacosta/CALLHOME/update_tun0_ipname.py >> /tmp/update_tun0_ipname.log 2>&1
```

<b>UPDATE_STATUS_PANEL.PY</b><br>
Run script to check VPN connection and update status panel accordingly every 05 min.
```bash
*/5 * * * * /usr/bin/python /home/dacosta/CALLHOME/update_status_panel.py >> /tmp/update_status_panel.log 2>&1
```
Troubleshoot or check cronjob run status in here /tmp/update_status_panel.log<br>
Rememeber to update this with your local path /home/user/folder/update_status_panel.py<br>
You can use "which python" to see where is the full path for python binary<br>
For me is /usr/bin/python

<b>UPDATED_INTERFACES_PY</b><br>
myip.py scripts tell us on startup what are the at the moment associated IP addresses for WIRED, WLAN and Tunnel VPN for Raspberry device, but what<br> if the device reboots or changes any of those IP addresses somehow? This script grabs current network scenario and compares to a previous file<br> having prior network configuration, if there's any change, this scripts sends out an e-mail advising us what has changed.<br>

<b>SYNC_SERVICES_SCRIPTS.SH</b><br>
I've just created a job that runs every hour to sync services settings in /etc/systemd/system/<br>
It basically grabs each service content and copies to a similar file inside Github repo folder to allow project syncness.<br>
```bash
cat /etc/systemd/system/myip.service >/home/dacosta/CALLHOME/SERVICES/myip.service

```

<b>SERVICES</b><br>
At least in Raspberry PI, services files/settings are store in /etc/systemd/system <br>

How to add a service?<br>
```bash
sudo nano /etc/systemd/system/service_filename
```
I am used to create files with .service extension, like ovpnscript.service<br>

<b>MANIPULATING SERVICES AFTER CREATION/UPDATE</b><br>
EXAMPLES<br>
```bash
sudo systemctl enable ovpnscript.service 
sudo systemctl start ovpnscript.service 
sudo systemctl status ovpnscript.service
sudo systemctl stop ovpnscript.service 
sudo systemctl disable ovpnscript.service 
sudo systemctl daemon-reload 
```

1) //enable service after file creation
2) //start service
3) //check service status
4) //stop service
5) //disable service
6) //when changes are applied to service file, it'll be requested to update is daemon

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
```bash
sudo nano /etc/systemd/system/autossh.service
```
This service script is save under SERVICES/autossh.service in this repo
```bash
sudo systemctl enable autossh
sudo systemctl start autossh
```
Stopping an autossh instance manually
```bash
sudo systemctl stop  autossh
killall autossh
```
<h1>STEPS TO SETUP THIS PROJECT IN YOUR ENVIRONMENT</h1><br>
```bash

```
Settings associated with SSH Server are available at<br>
https://github.com/dacostapiece/callhome_ssh_server<br>
If you "local device" is Windows, there's a project for that available at<br>
https://github.com/dacostapiece/callhome_windows<br>

<h1>TROUBLESHOOTING</h1>
<b>SAMPLE SIMPLE CURL</b><br>
<b>So you can test API communication with Atlassian</b>b<br>

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

Remember to replace values between brackets { } for your correspondinds IDs.
