<h1>CALLHOME</h1>
<h2>Raspberry /Linux Local device</h2>
<b>RFE</b><br>
1) Enable hotspot if no LAN or WLAN is unavailable (No known WLAN creds and/or range reachable)<br>
2) Handle multiple interfaces from single type - two VPNs, more than one ETH, etc...<br>
3) Start Webserver to receive SSID and password creds to login to neighbouring SSID<br>
4) Clean code<br>
5) Iterate loop only on associated components IDs<br>
VPN Checks VPNs Incidents related, SSH  Checks SSH Incidents related, and so on.<br>
6) Improve SSH handling in SSH External Server - handle stale processes<br>
7) Create an Install script<br>

<h2>OBJECTIVE</h2>
<b>Imagine you need to connect to a remote device, and here called Raspberry/Local Linux device which, <br>
through this device you are able to reach things<br> 
through it for networking troubleshooting, pentesting, monitoring and etc... on the remote network.<br></b>

1) How do you remote connect to this device?<br>
2) This remote connection has an independent backup for remote access?<br>
3) How do i know current device IP addresses? If i am remote or local next to it, how to connect to this device over LAN, WLAN or VPN? <br>
Does this info updates whenever any of these IP addresses changes?<br>
4) How do you know from two different perspectives if this device/setup/services are available?<br>

<b>With this project, you will connect it back to a device that's remotely plugged in a network, this settings will:</b><br> 
1) Send mail notification with device's WLAN, LAN, VPN IP addresses on startup and at every IP address change;<br>
2) Device will connect over VPN and SSH connection with two different independent sites and expose to us its SSH and VNC ports for remote access<br>
3) This project allows us to monitor these two connections from Raspberry to VPN Server and External SSH Server, as well as monitor connections<br> from a External SSH Server if VPN and SSH connections back to Raspberry device are working properly<br>
4) This monitoring will advise us over e-mail notification and with an External and third independent Web Status panel, so we can open this<br> panel and see it right away if any of ours services are working or not<br>
5) This project will update frequently a Fully Qualified Domain Name (FQDN) to expose a fixed way to connect to the device - so we don't need<br> to update our client settings for connections for VNC/SSH connections whenever VPN IP address changes<br>
6) As long as the device and you are connected to same VPN Server OR the device and you are connected to the same SSH Server - you will be <br>able to remotely reach this device.<br>
<br><b>Basically having a persistance way to reach the remote network through this device.</b><br>

<h2>##[DIAGRAM OVERVIEW]</h2>
<img src="https://github.com/user-attachments/assets/dea8d28e-2cf5-4d25-9319-7fe015105d34" />

<h2>FILES DESCRIPTION</h2>
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

<b>CHECK_INCIDENT_STATUS.PY</b><br>
This script will retrieve will check if there's any existing unresolved incidents for VPN in Atlassian Status Panel, save the JSON API response to a file and return component id (which service the incident is associated with) and incident id, if there's any
This script follows same logic for SSH service.

<b>CONFIG.PY</b><br>
This script holds overall settings for the project that aren't sensitive 

<b>.ENV</b><br>
This script holds overall settings for the project that are sensitive<br>
<b>.env isn't syncing to this github repo, remember creating it, there's a template in the "how to guide" in following sections.</b><br>

<b>CREATE_INCIDENT_VPN.PY</b><br>
This script will create an incident in Atlassian Status Panel, if a failure condition is met.

<b>DNS.PY</b><br>
This file tests my Raspberry device capability of DNS resolution. It's a punctual need for my environment, you can ignore it.<br>

<b>FIXNAMESERVERS.SH</b><br>
This scripts fixes my Raspberry device DNS settings every hour, my home router messes it up, i believe it's due to IPv6 advertisement or some sickness like this, pinpointing root cause was pretty annoying, so i worked around of it, please ignore this file.<br>
If you feel like using it, it requires root privileges. It's out of this project scope to show you how.

<b>.GITIGNORE</b><br>
This file holds which files and folders shoud not be syncing to github repo.<br>

<b>MYIP.PY</b><br>
This script will retrieve device ip addresses from Raspberry/Remote Linux device and send out an e-mail with WIRED, WLAN and TUNNEL VPN addresses along with whole IFCONFIG in mail body message.

If tun0 has no IP address, it will send out an e-mail with error
Logs for this script are stored in /tmp/myip.py.log

Code also calls writenadreadip_tunip.py - writeip funcion to write to a file the current tun ip address. This information will be used for another python script later on.

<b>MYIP_SCRIPT.SH</b><br>
Shell script that waits 30 secs after reboot (as it's set as startup service) to call myip_script.sh and myip.py. I now know i could set up a service to call myip.py directly, but this is how it was setup, it'll be as is.

myip.service, myip_script.sh and myip.py has the goal to tell us by sending out an email on startup what are the available IP addresses for remote access into raspberry device.

<b>__pycache__</b><br>
Codes are syncing to a place where codes are actually running, this folder is generated from python running. This folder is set to not sync with Github.

<b>OPENVPN_SCRIPT.SH</b><br>
Script run openvpn - passing creds already<br>
We have set up a service ovpnscript.service that calls openvpn_script.sh which is basically sending out in terminal a command line to establish a SSLVPN connection with a remote VPN Server - here called by reference purpose hub.example.com  
```bash
sudo openvpn --config /home/user/folder/file.ovpn --auth-user-pass /home/user/folder/pass.txt
```

You should have your own OpenVPN Server, so you can retrieve *.ovpn OpenVPN profile file along with its credentials for VPN connection.

<b>PASS.TXT</b><br>
OpenVPN Creds - format<br>

```bash
domain\username or username
password
```

<b>*.OVPN</b><br>
Your OpenVPN profile file. It's used for connection to hub.example.com

<b>*.ovpn and pass.txt aren't syncing to this github repo, remember creating them (creds file and grabbing your corresponding OVPN file), save 'em in the desired folder, prefarable callhome folder and adjust setting within openvpn_script.sh.</b><br>

<b>SENDMAIL.PY</b><br>
This script works as a module called by myip.py and updated_interfaces.py which will send out an email with WIRED, WLAN and TUNNEL VPN addresses along with whole IFCONFIG in mail body message.

<b>SEND_CURRENT_RASP_IP.PY</b><br>
This script will recover current Raspberry device IP address for Tunnel VPN and a create a file in SSH Server, <br>
another script will read this file in the SSH Server and knows which IP address to ping it back to test "Callback VPN" connection from SSH Server to Raspberry itself<br>

<b>SYNC_SERVICES_SCRIPTS.SH</b><br>
I've just created a job that runs every hour to sync services settings from /etc/systemd/system/ to /home/user/repo/SERVICES/

<b>TUNNEL_CONNECTION.PY</b><br>
This script will check if VPN or SSH is available.

<b>UPDATED_INTERFACES_PY</b><br>
myip.py scripts tell us on startup what are the at the moment associated IP addresses for <b>WIRED, WLAN and Tunnel VPN</b> for Raspberry device, but what<br> if the device reboots or changes any of those IP addresses somehow? This script grabs current network scenario and compares to a previous file<br> having prior network configuration, if there's any change, this scripts sends out an e-mail advising us what has changed.<br>

<b>UPDATE_INCIDENT_VPN.py</b><br>
This script will update an existing incident to solve it in Atlassian Status Panel, if a failure no longer exists. <b>VPN or SSH service</b>.

<b>UPDATE_STATUS_PANEL.PY</b><br>
https://dacostapiece.statuspage.io/ <br>
This script will  check <b>IF</b> <br>
1) tun0 (VPN) is available and if we are able to ping a remote vpn target, in our configuration<br>
it's pinging VPN Gateway private IP address, so not only we ensure VPN is active, but it's also working properly and <br>
2) Checks if SSH Server is reachable, here in the example - server.example.com. <br>
It's basically checking if primary connection over VPN and secondary connection over<br>
SSH are working from the perspective of Raspberry/Linux local device.<br>

The main goal is having a way to check wether VPN is working or not over a Status Web panel as well as triggering email alerts about failure incidents and restored services by Atlassian Status Panel.

You'll have to setup an account on Atlassian Status panel, it's free, to have this feature working.

<b>Logics</b><br>
VPN<br>
A) If VPN is working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, 
if there's any, solve that incident, VPN is working.<br>
B) If VPN is not working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service,<br>
if there's any, just keep it, VPN is not working.<br>
C) If VPN is not working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, <br>
if there's none, create an incident, VPN is not working.<br>
D) If VPN is working, check if there are existing open incidents in Atlassian Status Panel associated to VPN Service, <br>
if there's none, do nothing, VPN is working.<br>

<b>SSH</b><br>
This script follows same logic for SSH service.<br>

This scripts runs on startup with vpnstatuspanel.service<br>
And runs every 05min as cronjob<br>

<b>UPDATE_TUN0_IPNAME.PY</b><br>
This script will retrieve tun0 IP address and update a FQDN in Cloudflare through API, <br>
so we can always reach it back the device over VPN without<br>
needing to know its current IP address, neither updating clients settings like SSH, VNC, etc...<br>

In this example is <b>raspberry.example.com</b><br>
This scripts runs on startup with updatedns.service<br>
And runs every 05min as cronjob<br>

<b>Give permission for files to be run</b><br>
Example - repeat this process or call chmod +x *.py/chmod +x *.sh on the folder where scripts are stored.<br>
```bash
chmod +x /home/dacosta/CALLHOME/openvpn_script.sh
```
<b>WRITEANDREADIP.PY</b><br>
This script will read an existing file and it will write it to a file.<br>

<h2>HOW SCRIPTS ARE CALLED?</h2>
Some scripts are call by cronjobs, because they required recurring calls, some scripts are run by service, <br>
it runs on device startup or only once and other scripts are simply called by others scripts in chain.

<h2>CRONJOBS</h2>
<h2>##[DIAGRAM OVERVIEW CRONJOBS]</h2>
<img src="https://github.com/user-attachments/assets/7753ec31-0ae4-47c9-9e1d-f7f67be8f7d8" />

<b>AUTOSSH_SCRIPT_PY CRONJOB</b><br>
This is script is responsible to start and maintain an SSH connection to an outside server here called server.example.com<br>
Through this connection Raspberry/Linux local device will connect to and exposed its own SSH service (terminal access) and VNC (graphical access)<br>
This script runs as a service to make it "available" since startup and runs as a job, because it was a bit nasty creating a persistance with this running solely as service.<br>

<b>SYNC_SERVICES_SCRIPTS.SH CRONJOB</b><br>
I've just created a job that runs every hour to sync services settings in /etc/systemd/system/<br>
It basically grabs each service content and copies to a similar file inside Github repo folder to allow project syncness.<br>

<b>UPDATED_INTERFACES_PY CRONJOB</b><br>
myip.py scripts tell us on startup what are the at the moment associated IP addresses for <b>WIRED, WLAN and Tunnel VPN </b>for Raspberry device, but what if the device reboots or changes any of those IP addresses somehow? This script grabs current network scenario and <br>
compares to a previous file having prior network configuration, if there's any change, this scripts sends out an e-mail <br>
advising us what has changed.<br>


<b>UPDATE_TUN0_IPNAME.PY CRONJOB</b><br>
Update FQDN with current IP address at every 5min. It runs as regular raspberry user<br>
Error outputs are appended to file tmp/update_tun0_ipname.log<br>

<b>UPDATE_STATUS_PANEL.PY CRONJOB</b><br>
Run script to check VPN connection and update status panel accordingly every 05 min.

<b>Troubleshoot or check cronjob run status in here /tmp/update_status_panel.log<br>
Rememeber to update this with your local path /home/user/folder/update_status_panel.py<br></b>
You can use "which python" to see where is the full path for python binary<br>
For me is /usr/bin/python

<h2>SERVICES</h2>
<h2>##[DIAGRAM OVERVIEW SERVICES]</h2>
<img src="https://github.com/user-attachments/assets/25f3e19e-61f7-4d39-9847-18c4723344ab"/>

At least in Raspberry PI, services files/settings are store in /etc/systemd/system <br>

<b>How to add a service?</b><br>
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

<b>What does it each do above?</b>
1) enable service after file creation
2) start service
3) check service status
4) stop service
5) disable service
6) when changes are applied to service file, it'll be requested to update is daemon

<b>Note:</b> If VPN is connected by this service and you stop it, it will be same as closing a running program.<br>

<b>AUTOSSH.SERVICE</b><br>
File autossh.service<br>
The service will wait 30 seconds before start, it will call autossh_script.py, it will restart always. 
This service is forking so is able to call the script, runs autossh command and leave it in the background.<br>

<b>MYIP.SERVICE</b><br>
File myip.service<br>
The service will wait 30 seconds before start, it will call myip_script.sh, it will restart on failure, but only six times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 60 seconds before trying again and it will as run regular user.<br>

<b>OVPNSCRIPT.SERVICE</b><br>
File ovpnscript.service<br>
The service will start right away, it will call openvpn_script.sh, always run and it will be run as regular user.<br>

<b>UPDATEDNS.SERVICE</b><br>
File updatedns.service<br>
The service will wait 30 seconds before start, it will call update_tun0_ipname.py, it will restart on failure, but only three times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 30 seconds before trying again and it will run as regular user.<br>

<b>VPNSTATUSPANEL.SERVICE</b><br>
File vpnstatuspanel.service<br>
The service will wait 30 seconds before start, it will call update_status_panel.py, it will restart on failure, but only three times, it won't try to run after this. Service will fail as an example, if the VPN isn't connected yet. The service will delay 30 seconds before trying again and it will run as regular user. Here we set the WorkingDirectory - not sure if it's required.<br>

Backup connection method - a plan B method to persist remote access to raspberry over internet, in case, vpn fails

<b>SSH KEYS</b><br>
Autossh requires ssh keys to be set in order to work.

This service script is save under SERVICES/autossh.service in this repo

Stopping an autossh instance manually
```bash
sudo systemctl stop  autossh
killall autossh
```

<b>More instructions in how to handle autossh service among others, below</b>

<h1>STEPS TO SETUP THIS PROJECT IN YOUR ENVIRONMENT</h1>

1) Get you API Token ID from in your Cloudflare account with associated FQDN domain<br>
a) Create or log to your Cloudflare account<br>
b) Associate or used an already associated FQDN domain in your Cloudflare account<br>
Here exemplified by: example.com<br>
c) Go to:<br>
https://dash.cloudflare.com/profile/api-tokens/<br>
d) Select Create Token in API Tokens<br>
e) Choose Edit Zone DNS and click on Use Template<br>
f) Choose permissions Zone/DNS/Edit<br>
g) Choose resources Include/Specific zone/example.com<br>
h) Continue to summary<br>
i) Create Token<br>
j) Copy token<br>

https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids<br>
https://developers.cloudflare.com/fundamentals/api/get-started/create-token<br>
https://dash.cloudflare.com/profile/api-tokens<br>

2) Get your DNS Zone ID in your Cloudflare account with associated FQDN domain<br>
a) Log into your Cloudflare account<br>
b) Go to Websites/example.com<br>
c) On far right you'll see your Zone ID record<br>

3) Create three DNS Type A records without DNS proxy and TTL 5min in your Cloudflare account with associated FQDN domain.<br>
a) raspberry.example.com for VPN Tunnel Raspberry IP device<br>
You can set whatever IPv4 address, just for sake of creation of this DNS record<br>
After create, we'll edit it just to create an audit log for later purpose<br>
b) server.example.com for External SSH device<br>
Set External SSH Server Public IP address for this DNS record<br>

<b>Note:</b> You can create and associate a FQDN for you External SSH Server Public IP address or use an existing FQDN for it<br>

c) hub.example.com for VPN Server<br>
Set VPN Server Public IP address for this DNS record<br>

<b>Note:</b> You can create and associate a FQDN for you VPN Server Public IP address or use an existing FQDN for it<br>

d) Log into your Cloudflare account<br>
e) On left sidebar menu, go to Manage account/Audit log<br>
f) Expand recent audit logs for DNS changes and grab DNS record ID for raspberry.example.com.<br>
The DNS record ID will be simply called "id"<br>
Example<br>
```bash
{
  "content": "1.1.1.2",
  "data": {},
  "id": "your_dns_record_id",
  "name": "raspberry.example.com",
  "proxied": false,
  "settings": {},
  "ttl": 300,
  "type": "A",
  "zone_id": "your_dns_zone_id",
  "zone_name": "example.com"
}
```
https://community.cloudflare.com/t/cannot-find-record-id/326344<br>
<b>Don't misundertook zone id with dns record id</b><br>

4) You can use any SMTP Server to sending our own E-mail notifications. In our scenario we're going to an Gmail account<br>
a) Create a new or login to your existing Gmail account<br>
b) After validation or creation of new Gmail account, go to<br>
https://myaccount.google.com/apppasswords<br>

c) Give it a name and click on create<br>
d) The generated app password will popup to you, this password will be used in our script<br> 
to authenticate and send e-mails using our Gmail account<br>
e) You can always go back to same link and delete the password app if desired.<br>
<br>
5) Setting up your Status Page panel from Atlassian<br>
a) Go to https://www.atlassian.com/software/statuspage<br>
b) Create your free account<br>
c) Choose subdomain name in your Atlassian account<br>

<b>Example</b><br>
examplepanel.atlassian.net<br>

Click next if possible, THIS IS NOT you Status Panel page, it's something else under the Umbrella of Atlassian/Jira cloud services<br>
d) It may be requested (currently it's for new accounts) a component creation in a setup wizard<br>
We're going to need four components, here they are:<br>
<br>
<b>OpenVPN Outbound Raspberry Device</b><br>
Description: The primary VPN connection from Raspberry device to HUB VPN Gateway<br>
<br>
<b>SSH Tunnel Outbound Raspberry Device</b><br>
Description:The secondary VPN connection over SSH Tunnel from Raspberry device to External SSH Server.<br>
<br>
<b>External OpenVPN Raspberry Device Check</b><br>
Description: This component checks externally from SSH Server if VPN connection to Raspberry is working. <br>
It will connect to same VPN HUB device and try pinging Raspberry current tunnel IP address.<br>

<b>External SSH Tunnel Raspberry Device Check</b><br>
Description: This component checks externally from SSH Server <br>
if the callback SSH Tunnel connection to Raspberry is working. It will try to connect to Raspberry SSH Service.<br>

<i>If requested, you don't need to setup a Component group. <br>
You can leave as it is or play with it later on as pleased. This project doesn't use Component group.<br>

If Components wouldn't be requested at the new account startup, you'll need to setup them later.<br></i>

e) In the current situation, after four components were added, just click Next<br>
f) Upload a Status Panel image logo or click Next, you can add it later on<br>
g) Setup e-mail to receive UPs and Downs regarding your components/services - click Send test email<br>
For me it didn't workout sending out a test email through Atlassian new account wizard. <br>
When i first used Status Page, i added manually on own.<br>
While writing this doc, i've just realized admin notification from Atlassian Status Panel <br>
it seems to have two different approaches.<br>

g.1) Remind admins of ongoing incident - standard every 3, 6, 12 and 24 hours <br> 
This notification will be sent to e-mail account associated to your Atlassian account<br>
g.2) For our project and to receive at the moment incident notification from Atlassian, <br>
you have to subsbribe it. You can choose whatever e-mail account you might like receiving those email notifications.<br>
We suggest you use the recent created Gmail account or any e-mail address that it's supposed to receive those notifications<br>
g.3) Subscribing to your own Status Panel, click on View status page<br>
g.4) In our example, it opens up page: https://examplepanel.statuspage.io/<br>
g.5) Select Subscribe to Updates<br>
g.6) Enter your e-mail address - i haven't tested other subscription options like x.com - you can try it later<br>
g.7) Go to your e-mail account, open up Confirm you subscription mail message and click on Confirm<br>
g.8) You'll be redirected to Status Panel page with an advise that confirmation was sucessful<br>
g.9) There you go, anytime an incident occurs or get its clear, you'll receive an e-mail message.<br>
<br>
6) Get your API Token and Page ID for Atlassian Status Panel<br>
a) Go to Upper right "power" button and click it for change Settings<br>
b) Select API info<br>
c) Create key - give it a name - you call it whatever you like, i suggest "Callhome"<br>
d) Take note of your API Key for Atlassian Status Panel<br>
e) On same page you'll have down below the page next to Page IDs, your Page ID, take a note of it<br>
<br>
h) Invite a team member - it suggests you to do it, i haven't done. I'll suggest you to skip it for now, click Next.<br>
i) Save and exit to conclude Wizard<br>
j) On Status Page, click on Activate your page and select FREE plan, confirm role based warning telling you Free plan doesn't <br>
we wont need it<br>


7) Get your Component IDs in Atlassian Status Page<br>
We'll retrieve four Component IDs, two for the Raspberry/Linux local device and two for the External SSH Server<br>

Their variables we'll update them accordingly later in config code<br>

<b>Raspberry/Linux local device</b><br>
raspberry_vpn_component_id<br>
remote_ssh_server_component_id<br>

<b>External SSH Server</b><br>
callback_vpn_component_id<br>
callback_ssh_component_id<br>

a) Click on Components<br>
b) Here you can Add component - if you haven't on Startup Atlassian account Wizard and follow previous formentioned steps<br>
c) There are two "builtin" Components, you can delete them, they are the for example purposes<br>
d) Click on OpenVPN Outbound Raspberry Device component<br>
d.1) You'll be able to grab this Component ID from the URL formatting, here exampled by:<br>

```bash
https://manage.statuspage.io/pages/{your page id}/components/{your current component id}/edit
```

d.2) Or going down on the page, next to Component API ID and copying it, take a note.<br>
Here a table so you can follow along and do not get confused by.<br>
<h2>[TABLE]</h2>
<b>Component IDs below are just samples, you'll have your own</b>

| **Component Name**                      | **Component Variable**           | **Component ID**       |
| --------------------------------------- | -------------------------------- | ---------------------- |
| OpenVPN Outbound Raspberry Device       | `raspberry_vpn_component_id`     | `abcdefghijklm`        |
| SSH Tunnel Outbound Raspberry Device    | `remote_ssh_server_component_id` | `nopqrstuvwxyz`        |
| External OpenVPN Raspberry Device Check | `callback_vpn_component_id`      | `zyxwvutsrqponm`       |
| External SSH Tunnel Raspberry Device Check | `callback_ssh_component_id`   | `lkjihgfedcba`         |


You'll repeat this process to get all four Component IDs.

8) Clone and/or download this repository (callhome) under desired folder in your local linux device, here in our example, <br>
a raspberry device.
If downloaded, remember unzip its folder
```bash
unzip file.zip -d /path/to/destination
```
a) Take note of the complete full path from this repository - you can call "pwd" inside the directory to get its full path location

```bash
pwd
/home/user/callhome
```

9) Setup SSH Settings for Remote Access IN Raspberry<br>
a) For Raspberry, the most easy is<br>
b) Access it over GUI in virtual machine/HDMI monitor<br>
c) Click on Raspberry icon upper left/Preferences<br>
d) Click on Raspberry PI Configuration<br>
e) On Interfaces tab, toggle ON for SSH<br>
IF Available On Interfaces tab, toggle ON for VNC for remote GUI access<br>
IF VNC option doesnt show, google it how to enable VNC or if you dont want, just ignore VNC step<br>
f) SSH user and password creds are the same you setup (or standard?) for raspberry device<br>
<br>

IF <b>YOUR LOCAL DEVICE</b> is not a Raspberry PI, here an example to setup SSH Server for Kali Linux.<br> 
If SSH isn't already enable on your local device, please google it how to enable it<br>

```bash
sudo apt-get update
sudo apt-get install ssh
sudo systemctl enable ssh
sudo service ssh start
```
<h2>External SSH Server</h2>
10) Setup SSH Settings for External SSH Server<br>
Callhome SSH Server repository<br>
https://github.com/dacostapiece/callhome_ssh_server<br>
<br>

Here an example to setup SSH Server for Kali Linux.<br> 
If SSH Server isn't already enabled on your local device, please google it how to enable it<br>

```bash
sudo apt-get update
sudo apt-get install ssh
sudo systemctl enable ssh
sudo service ssh start
```

11) Allow SSH Public Key Authentication
a) Edit sshd_config settings file
Usually at
/etc/ssh/sshd_config
```bash
sudo nano /etc/ssh/sshd_config
```
<b>sudo if root is required on your SSH Server Linux Distro - Kali Linux does require<br></b>

b) Find line <b>PubAuthenticationKey</b>, uncomment if necessary (remove #) and set it to yes<br>
c) Find line <b>PasswordAuthentication</b>, uncomment if necessary (remove #) and set it to no<br>
<b>Disable Password Authentication</b> if password ssh access should not be available or ignore this step

<h2>Raspberry/Local Linux Device</h2>

12) Setup SSH Keys for SSH Reverse Tunnel between Raspberry and External SSH Server<br>
Commands are shown below<br>

a) Call ssh key generator<br>
If you type a desired name for ssh key pair, but you don't specify full path directory, <br>
key pair will be saved on the current directory your user is at<br>
You can type "pwd" to check current full path directory<br>

b) Enter file name with full path or hit enter to maintain default<br>
c) Enter SSH key password, if you hit enter with blank password, no password will be set, <br>
for sake of current project, please set a password and take note<br>
d) Repeat password if it was entered before<br>

<b>Notes</b><br>
Key with .pub - public key<br>
Key without extension - private key<br>

<b>Commands</b><br>
ed25519 or preferable encryption algorihtm for SSH Key
```bash
ssh-keygen -t ed25519
```

13) Share SSH public key to External SSH Server<br>
Do it once you already have setup and SSH creds for External SSH Server (steps 10 and 11 from here)<br>
```bash
ssh-copy-id -i /path/to/custom_key.pub username@remote_server
```
If ssh-copy-id is unavailable, cat your file.pub (SSH Key public key) content and save it at on External SSH Server<br>

```bash
/home/user/.ssh/authorized_keys
```

If this file doesn't exist, create it on External SSH Server<br>
You can test this authentication<br>
<b>Most simple and manual SSH Key test</b><br>

a) Flag -i indicate private key location followed by username and reachable External SSH Server address<br>

```bash
ssh -i /home/user/.ssh/keyfile user@server.example.com
```
//enter your SSH key password, if password key was set before<br>

<b>SSH Key test with SSH Agent</b><br>
b) Enable SSH Agent with Environment Variable<br>
c) Add desired PRIVATE KEY file here exampled by "keyfile"<br>
d) Enter password if the SSH Key was password encrypted<br>
e) Try SSH into External SSH Server passing the private key already (From SSH-Agent)<br>
```bash
eval "$(ssh-agent -s)"
ssh-add /home/user/.ssh/keyfile
ssh user@server.example.com
```

14) Create an .env file using template below inside your download repository folder (Raspberry/Linux local side)<br>

<b>.ENV file template</b><br>
```bash
#.env
#remove { } brackets whenever they appear here, they are just pointing you should paste your ID/API Token
# Mail settings
mailserver = 'smtp.gmail.com'
smtpport = 587
mailusername = 'yourgmailaccount@gmail.com'
mailpassword = 'yourappgmailaccount'
#it's not your actual gmail account password
source_mailaddress = 'yourgmailaccount@gmail.com'
dest_mailaddress = 'yourgmailaccount@gmail.com'
#You should repeat source and dest mail address for the sake of easeness, but you can change it as required

# Remote VPN Target
vpn_probe_target = "192.168.0.1"
#This is the IP address for your primary and private internal VPN Server itself, change it accordingly

#API Atlassian General Settings
api_token = "{your API token}"
page_id = "{your Atlassian page ID}"

# Cloudflare API credentials
CF_API_TOKEN = '{your recent API Token created in Cloudflare}'

# Cloudflare Zone ID and DNS record information
ZONE_ID = 'abcdefghijklmnopqrstuvwxyz'
#your just found DNS zone ID for the domain you're using it'
DNS_RECORD_NAME = 'raspberry.example.com'
DNS_RECORD_ID = 'abcdefghijklmnopqrstuvwxyz'
#your just found DNS record ID for the raspberry fqdn domain name you'll use it for raspberry

# SSH settings
SSH_USER = 'ssh user you have setup for External SSH Server'
SSH_SERVER = 'server.example.com'
SSH_OPTIONS = '-M 0 -f -N -R 2220:localhost:22 -R 5910:localhost:5900 '
#This SSH Options are exposing SSH with external port 2220 and VNC with external port 5910, taking in mind local VNC port is 5900, sometimes it can be 5901, 5902, etc...
#Check it which is yours VNC raspberry/local device local port - IF you'll expose VNC for External GUI remote access
#You can change the exposed ports to something mor suitable for you, here they are 2220 for SSH and 5910 for VNC

SSH_KEY_PASSWORD='ssh key password you have setup for External SSH Server'
#This is the password for SSH KEY, not the SSH USER PASSWORD, we won't be using SSH USER PASSWORD for Login

KEY_FILE = '/home/user/.ssh/idrsa'
#The location along filename for your SSH PRIVATE KEY you'll use and have added to known hosts in External SSH Server

SSH_PORT = 22
#The exposed SSH Server port, SSH standard is 22

#SSH SERVER
SSH_SERVER_FILENAME = "current_rasp_ip.txt"
#SSH Server you read this file that's going to be WRITTEN over SSH connection from Raspberry/local device to SSH Server, this file will contain the raspberry tunnel ip address, so SSH Server knows where to ping it back to verify externally if Raspberry is indeed connected to Primary VPN Server

ssh_server_filename_directory = "/home/user/CALLHOME_SSH_SERVER"
#The place where you write the above file over SSH connection in the External SSH Server
```

Which settings you can leave as it is .ENV file? (at least in most cases)<br>
a) SSH_OPTIONS<br>
b) SSH_PORT<br>
c) SSH_SERVER_FILENAME<br>

Everything else you'll need to update according to your environment.<br>

15) Adjust config settings (Raspberry/Linux local side)<br>
config.py file<br>
a) raspberry_vpn_component_id<br>
b) remote_ssh_server_component_id<br>

Settings associated with SSH Server are available at<br>
https://github.com/dacostapiece/callhome_ssh_server<br>

If you "local device" is Windows, there's a project for that available at<br>
https://github.com/dacostapiece/callhome_windows<br>

16) Enabling python libraries<br>
a) ping3<br>
b) python-dotenv<br>
c) requests<br>
d) pip<br>
e) autossh<br>

Install pip
```bash
sudo apt install python3-pip
```
Install autossh
```bash
sudo apt install autossh
```
Install libraries
pip has to be installed as previous step, so you can move on command below
```bash
pip3 install ping3 python-dotenv requests
```
Fix PATH for dotenv and ping3
```bash
nano ~/.bashrc
```
Add this to end of file
```bash
export PATH="$HOME/.local/bin:$PATH"
```
Refresh and validate it
```bash
source ~/.bashrc
echo $PATH
```
17) Set OpenVPN<br>
a) Install OpenVPN client
```bash
sudo apt install openvpn
```
b) Download you file.ovpn OpenVPN profile given by VPN Server administrator and/or yourself<br>
c) Create your OpenVPN credential file, here as pass.txt
```bash
username or domain\username
password
```

d) Test it, connect to it and ping it the private VPN internal address
```bash
 sudo openvpn --config callhome.ovpn --auth-user-pass pass.txt
```

18) If you haven't setup your <b>External SSH Server</b> so far, go start setting it up!</br>
https://github.com/dacostapiece/callhome_ssh_server<br>

19) Test APIs<br>
a) More below on troubleshooting you have sample and example for testing API Communication with Cloudflare and Atlassian <br>
20) Test SSH<br>
a) Steps 9 to 14 allow you to test SSH connection from Raspberry to External SSH Server<br>
b) You can locally test if Raspberry is accepting SSH connections or not<br>

21) Enabling services<br>
Overall services handling - for each service - example
```bash
sudo systemctl enable autossh.service 
sudo systemctl start autossh.service 
sudo systemctl status autossh.service
sudo systemctl stop autossh.service 
sudo systemctl disable autossh.service 
sudo systemctl daemon-reload 
```


a) autossh.service<br>
a.1) Adjust your user and script path following sample below<br>
Sample script
```bash
[Unit]
Description=AutoSSH Tunnel Service
After=network.target

[Service]
ExecStartPre=/bin/sleep 30
Type=forking
ExecStart=/home/user/callhome/autossh_script.py
Restart=always
User=user
WorkingDirectory=/home/user/callhome

[Install]
WantedBy=multi-user.target
```
a.2) Save this settings following this command
```bash
sudo nano /etc/systemd/system/autossh.service
```
a.3) Setup services
```bash
sudo systemctl enable autossh.service 
sudo systemctl start autossh.service 
sudo systemctl status autossh.service
```

b) myip.service<br>
b.1) Adjust your user and script path following sample below
Sample script
```bash
[Unit]
Description=My Script

[Service]
ExecStartPre=/bin/sleep 30
ExecStart=/home/user/callhome/myip_script.sh
Restart=on-failure
StartLimitBurst=6
RestartSec=60
User=user
WorkingDirectory=/home/user/callhome
[Install]
WantedBy=multi-user.target
```
b.2) Save this settings following this command
```bash
sudo nano /etc/systemd/system/myip.service
```
b.3) Setup services
```bash
sudo systemctl enable myip.service 
sudo systemctl start myip.service 
sudo systemctl status myip.service
```


c) ovpnscript.service<br>
c.1) Adjust your user and script path following sample below
Sample script
```bash
[Unit]
Description=OpenVPN Script - Persistance

[Service]
ExecStart=/home/user/callhome/openvpn_script.sh
Restart=always
User=user

[Install]
WantedBy=multi-user.target
```
c.2) Save this settings following this command
```bash
sudo nano /etc/systemd/system/ovpnscript.service
```
c.3) Setup services
```bash
sudo systemctl enable ovpnscript.service 
sudo systemctl start ovpnscript.service
sudo systemctl status ovpnscript.service
```

d) updatedns.service<br>
d.1) Adjust your user and script path following sample below
Sample script
```bash
[Unit]
Description=My Script

[Service]
ExecStartPre=/bin/sleep 30
ExecStart=/home/user/callhome/update_tun0_ipname.py
Restart=on-failure
StartLimitBurst=3
RestartSec=30
User=user

[Install]
WantedBy=multi-user.target
```
d.2) Save this settings following this command
```bash
sudo nano /etc/systemd/system/updatedns.service
```
d.3) Setup services
```bash
sudo systemctl enable updatedns.service 
sudo systemctl start updatedns.service
sudo systemctl status updatedns.service
```

e) vpnstatuspanel.service<br>
e.1) Adjust your user and script path following sample below
Sample script
```bash
[Unit]
Description=My Script
After=network.target

[Service]
ExecStartPre=/bin/sleep 30
ExecStart=/home/user/callhome/update_status_panel.py
Restart=on-failure
StartLimitBurst=3
RestartSec=30
User=user
WorkingDirectory=/home/user/CALLHOME

[Install]
WantedBy=multi-user.target
```
e.2) Save this settings following this command
```bash
sudo nano /etc/systemd/system/vpnstatuspanel.service
```
e.3) Setup services
```bash
sudo systemctl enable vpnstatuspanel.service 
sudo systemctl start vpnstatuspanel.service
sudo systemctl status vpnstatuspanel.service
```

22) Enabling cron jobs<br>
To create/edit cronjobs, type 
```bash
crontab -e
```
 - then select your text editor (when crontab -e is called at first time), i am more familiar with nano

type 
```bash
sudo crontab -e
```

to call cronjobs as root user (not required for our current scripts)<br>
Then select your text editor (when crontab -e is called at first time), i am more familiar with nano<br>
<br>

<h1>Setting All Cronjobs at Once</h1>
Just copy and paste all below - correct user and repository names accordingly to your environment previously.

```bash
*/5 * * * * /usr/bin/python /home/user/callhome/autossh_script.py >>/tmp/autossh_script.job.log 2>&1
0 * * * * /home/user/callhome/sync_services_scripts.sh >>/tmp/sync_services_scripts.log 2>&1
*/5 * * * * /usr/bin/python /home/user/callhome/updated_interfaces.py >>/tmp/updated_interfaces_cron.log 2>&1
*/5 * * * * /usr/bin/python /home/user/CALLHOME/update_tun0_ipname.py >> /tmp/update_tun0_ipname.log 2>&1
*/5 * * * * /usr/bin/python /home/user/CALLHOME/update_status_panel.py >> /tmp/update_status_panel.log 2>&1
```

<h3>Setting One at Time</h3>
<b>If you have setup all at once, you can skip next steps</b><br>
<br>
a) autossh_script.py<br>
a.1) Adjust your user and script path following sample below
```bash
*/5 * * * * /usr/bin/python /home/user/callhome/autossh_script.py >>/tmp/autossh_script.job.log 2>&1
```

b) sync_services_scripts.sh<br>
b.1) Adjust your user and script path following sample below
```bash
0 * * * * /home/user/callhome/sync_services_scripts.sh >>/tmp/sync_services_scripts.log 2>&1
```

c) updated_interfaces.py<br>
c.1) Adjust your user and script path following sample below
```bash
*/5 * * * * /usr/bin/python /home/user/callhome/updated_interfaces.py >>/tmp/updated_interfaces_cron.log 2>&1
```

d) update_tun0_ipname.py<br>
d.1) Adjust your user and script path following sample below
```bash
*/5 * * * * /usr/bin/python /home/user/callhome/update_tun0_ipname.py >> /tmp/update_tun0_ipname.log 2>&1
```

e) update_status_panel.py<br>
e.1) Adjust your user and script path following sample below
```bash
*/5 * * * * /usr/bin/python /home/user/callhome/update_status_panel.py >> /tmp/update_status_panel.log 2>&1
```

<h1>CALLHOME_SSH_SERVER</h1>
<h1>NOVA</h1>

<b>RFE</b><br>
1) Clean code<br>
2) Iterate loop only on associated components IDs - VPN Checks VPNs Incidents related, SSH  Checks SSH Incidents related, and so on.<br>
3) Improve SSH handling in SSH External Server - handle stale processes<br>
4) Create a Install script<br>

<h2>OBJECTIVE</h2>

[See section](https://github.com/dacostapiece/callhome/blob/main/README.md#objective)

<h2>[DIAGRAM OVERVIEW SSH SERVER]</h2>

[See section](https://github.com/dacostapiece/callhome/blob/main/README.md#diagram-overview)

<h2>SETTINGS FOR EXTERNAL SSH SERVER</h2>
This project holds settings for External SSH Server to be set along "callhome" project or "callhome windows" project for Windows OS
<b>CALLHOME</b><br>
https://github.com/dacostapiece/callhome/<br>
<br>
<b>CALLHOME WINDOWS</b><br>
https://github.com/dacostapiece/callhome_windows

<h2>FILES DESCRIPTION SSH SERVER</h2>

<b>CHECK_INCIDENT_STATUS_SSH_SERVER.PY</b><br>
This script will retrieve will check if there's any existing unresolved incidents for VPN (connection against Raspberry device over VPN) in<br> Atlassian Status Panel, save the JSON API response to a file and return component id (which service the incident is associated with) <br>
and incident id, if there's any
This script follows same logic for SSH service (connection against Raspberry device over SSH Reverse Tunnel).

<b>CONFIG_SSH_SERVER.PY</b><br>
This script has all required settings to be adjusted, except by sensitive information settings in .ENV file.

<b>CREATE_INCIDENT_SSH_SERVER.PY</b><br>
This script will create an incident in Atlassian Status Panel, if a failure condition is met.

<b>OPENVPN.SH</b><br>
Script run openvpn - passing creds already<br>
We have set up a service ovpnscript.service that calls openvpn_script.sh which is basically sending out in terminal a command line <br>
to establish a SSLVPN connection with a remote VPN Server - here called by reference purpose hub.example.com<br>
Note: Here on the External SSH Server - we connect to the same VPN Server as Raspberry/Linux local device, so we can monitor <br>
if Raspberry/Linux local device itself is REACHABLE or not.

```bash
sudo openvpn --config /home/user/folder/file.ovpn --auth-user-pass /home/user/folder/pass.txt
```

You should have your own OpenVPN Server, so you can retrieve *.ovpn OpenVPN profile file as long as credentials for this VPN connection.

<b>PASS.TXT</b><br>
OpenVPN Creds - format<br>

```bash
domain\username or username
password
```

<b>*.ovpn and pass.txt are't syncing to this github repo, remember creating them (creds file and grabbing your corresponding OVPN file), save 'em in the desired folder, prefarable callhome_ssh_server folder and rename openvpn_script.sh.</b><br>

<b>SSH_HANDLER.PY</b><br>
This script will check every hour if there SSH connections above a specified limit number, if there is, it will log hour, number of connections and reboot External SSH Server for cleanup.

<b>SYNC_SERVICES_SCRIPTS.SH</b><br>
I've just created a job that runs every hour to sync services settings in /etc/systemd/system/<br>
It basically grabs each service content and copies to a similar file inside Github repo folder to allow project syncness.<br>

<b>TUNNEL_CONNECTION_SSH_SERVER.PY</b><br>
This script will check if VPN (connection against Raspberry device over VPN) or SSH (connection against Raspberry device over SSH Reverse Tunnel) is available.

<b>UPDATE_INCIDENT_SSH_SERVER.PY</b><br>
This script will update an existing incident to solve it in Atlassian Status Panel, if a failure no longer exists. VPN or SSH service.

Give permission for files to be run<br>
Example - repeat this process or call chmod +x *.py/chmod +x *.sh on the folder where scripts are stored.<br>
```bash
chmod +x /home/user/folder/openvpn_script.sh
```

<b>UPDATE_STATUS_PANEL_SSH_SERVER.PY</b><br>
https://examplepanel.statuspage.io/ <br>
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

Troubleshoot or check cronjob run status in here /tmp/update_status_panel.log<br>
Rememeber to update this with your local path /home/user/folder/update_status_panel.py<br>
You can use "which python" to see where is the full path for python binary<br>
For me is /usr/bin/python

<b>HOW SCRIPTS ARE CALLED?</b><br>
Some scripts are call by cronjobs, because they required recurring calls, some scripts are run by service, it runs on device startup or only once and other scripts are simply called by others scripts in chain.

<h2>CRONJOBS SSH SERVER</h2>
<h2>[DIAGRAM OVERVIER SSH SERVER CRONJOBS]</h2>
<img src="https://github.com/user-attachments/assets/2d94089f-86de-4361-996f-a2182337175f" />

<h2>SERVICES SSH SERVER</h2>
<h2>[DIAGRAM OVERVIER SSH SERVER SERVICES]</h2>
<img src="https://github.com/user-attachments/assets/286ce258-ceec-41b8-b68f-991a9ec955f5" />

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

<b>OVPNSCRIPT.SERVICE</b><br>
File ovpnscript.service<br>
The service will start right away, it will call openvpn_script.sh, always run and it will be run as regular user.<br>

<b>__pycache__</b><br>
Codes are syncing to a place where codes are actually running, this folder is generated from python running. This folder is set to not sync with Github.

<h1>##STEPS TO SETUP THIS PROJECT IN YOUR ENVIRONMENT SSH SERVER</h1>

<h2>External SSH Server - Linux Device</h2>

1) Clone and/or download this repository (callhome) under desired folder in your local linux device, here in our example, a raspberry device.
If downloaded, remember unzip its folder
```bash
unzip file.zip -d /path/to/destination
```
a) Take note of the complete full path from this repository - you can call "pwd" inside the directory to get its full path location
b) I recommend you rename whatever name this folder repository is to callhome_ssh_server
```bash
pwd
/home/user/callhome_ssh_server
```

2) Setup SSH Settings for External SSH Server<br>

Here an example to setup SSH Server for Kali Linux.<br> 
If SSH isn't already enable on your local device, please google it how to enable it<br>

```bash
sudo apt-get update
sudo apt-get install ssh
sudo systemctl enable ssh
sudo service ssh start
```

2) Allow SSH Public Key Authentication
a) Edit sshd_config settings file
Usually at
/etc/ssh/sshd_config
```bash
sudo nano /etc/ssh/sshd_config
```
#sudo if root is required on your SSH Server Linux Distro - Kali Linux does require
b) Find line PubAuthenticationKey, uncomment if necessary (remove #) and set it to yes
c) Find line PasswordAuthentication, uncomment if necessary (remove #) and set it to no - DO IT if password ssh access should be disabled or ignore this step

3) Create an .env file using template below inside your download repository folder (External SSH Server side)

<b>.ENV file template</b><br>
```bash
#.env
#remove { } brackets whenever they appear here, they are just pointing you should paste your ID/API Token

#IT MUST MATCH SAME FILENAME FROM RASPBERRY DEVICE
remote_ip_address_filename = "current_rasp_ip.txt"

#API Atlassian General Settings
api_token = "{your API token}"
page_id = "{your Atlassian page ID}"

# SSH SERVER settings
PORT_TO_CHECK = '2220'
SSH_TUNNEL_ADDRESS = 'localhost'

#SSH SERVER
SSH_SERVER_FILENAME = "current_rasp_ip.txt"
ssh_server_filename_directory = "/home/user/callhome_ssh_server"
```
You can follow steps on README.md file from repository callhome/callhome_windows to know how to retrieve your Atlassian info
https://github.com/dacostapiece/callhome/<br>
https://github.com/dacostapiece/callhome_windows/

Which settings you can leave as it is .ENV file? (at least in most cases)<br>
a) PORT_TO_CHECK<br>
b) SSH_TUNNEL_ADDRESS<br>
c) SSH_SERVER_FILENAME<br>

Everything else you'll need to update according to your environment.<br>

4) Adjust config settings (External SSH Server side)
config_ssh_server.py file<br>
a) callback_vpn_component_id<br>
b) callback_ssh_component_id<br>
<br>
Settings associated with Raspberry/Linux local device are available at<br>
https://github.com/dacostapiece/callhome<br>
<br>
If you "local device" is Windows, there's a project for that available at<br>
https://github.com/dacostapiece/callhome_windows<br>

5) Enabling python libraries<br>
a) ping3<br>
b) python-dotenv<br>
c) requests<br>
d) pip<br>
e) autossh<br>
<br>
Install pip
```bash
sudo apt update
sudo apt install python3-pip
```
Install libraries
pip has to be installed as previous step, so you can move on command below
```bash
pip3 install ping3 python-dotenv requests
```
Note: For Kali Linux, we had to make following change in order to ping3 work properly
```bash
sudo nano /etc/sysctl.conf
```
Then add to bottom file
```bash
net.ipv4.ping_group_range = 0 2147483647
```
Refresh it
```bash
sudo sysctl -p
```

Fix PATH for dotenv and ping3
```bash
nano ~/.bashrc
```
Add this to end of file
```bash
export PATH="$HOME/.local/bin:$PATH"
```
Refresh and validate it
```bash
source ~/.bashrc
echo $PATH
```
5) Set OpenVPN<br>
a) Install OpenVPN client<br>

```bash
sudo apt install openvpn
```
b) Download you file.ovpn OpenVPN profile given by VPN Server administrator and/or yourself<br>
c) Create your OpenVPN credential file, here as pass.txt<br>

```bash
username or domain\username
password
```
d) Test it, connect to it and ping it the private VPN internal address
```bash
 sudo openvpn --config callhome.ovpn --auth-user-pass pass.txt
```
e) Allow users in sudo to run without password prompt<br>
In order to call openvpn, we use sudo (in Kali Linux, Raspberry doesnt prompt it), but we can't pass kali's password when running openvpn as service

```bash
sudo apt install -y kali-grant-root && sudo dpkg-reconfigure kali-grant-root
```
Reference: https://www.kali.org/docs/general-use/sudo/


4) If you haven't so far, go start setting up Raspberry/Linux local device<br>
https://github.com/dacostapiece/callhome<br>
Or<br>
For Windows OS<br>
https://github.com/dacostapiece/callhome_windows<br>

5) Test APIs<br>
a) More below on troubleshooting you have sample and example for testing API Communication with Cloudflare and Atlassian <br>
6) Test SSH<br>
a) If Raspberry device is already connect to here with SSH and it's exposing its ports, you can:<br>
If you are following standard suggested settings<br>

```bash
ssh -p 2220 user@localhost
```
b) You can locally test if External SSH Server is accepting SSH connections or not<br>

7) Enabling services<br>
Overall services handling - for each service - example

```bash
sudo systemctl enable openvpn.service 
sudo systemctl start openvpn.service
sudo systemctl status openvpn.service
sudo systemctl stop openvpn.service
sudo systemctl disable openvpn.service 
sudo systemctl daemon-reload 
```

a) openvpn.service<br>
a.1) Adjust your user and script path following sample below<br>
Sample script

```bash
[Unit]
Description=OpenVPN Script - Persistance

[Service]
ExecStartPre=/bin/sleep 10
ExecStart=/home/user/callhome_ssh_server/openvpn.sh
Restart=always
User=user

[Install]
WantedBy=multi-user.target
```
a.2) Save this settings following this command

```bash
sudo nano /etc/systemd/system/openvpn.service
```
a.3) Setup services

```bash
sudo systemctl enable openvpn.service 
sudo systemctl start openvpn.service
sudo systemctl status openvpn.service
```

21) Enabling cron jobs<br>
To create/edit cronjobs, type

```bash
crontab -e
```

 - then select your text editor (when crontab -e is called at first time), i am more familiar with nano

You can use "which python" to see where is the full path for python binary<br>
For me is /usr/bin/python<br>

<h1>Setting All Cronjobs at Once SSH Server</h1>
Just copy and paste all below - correct user and repository names accordingly to your environment previously.<br>

```bash
0 * * * * /usr/bin/python /home/user/callhome_ssh_server/ssh_handler.py >> /tmp/ssh_handler_job.log 2>&1
0 * * * * /home/user/callhome_ssh_server/sync_services_scripts.sh >>/tmp/sync_services_scripts.log 2>&1
*/5 * * * * /usr/bin/python /home/user/callhome_ssh_server/update_status_panel_ssh_server.py >> /tmp/update_status_panel_ssh_server.log 2>&1
```


a) ssh_handler.py<br>
a.1) Adjust your user and script path following sample below
```bash
0 * * * * /usr/bin/python /home/user/callhome_ssh_server/ssh_handler.py >> /tmp/ssh_handler_job.log 2>&1
```

b) sync_services_scripts.sh<br>
b.1) Adjust your user and script path following sample below
```bash
0 * * * * /home/user/callhome_ssh_server/sync_services_scripts.sh >>/tmp/sync_services_scripts.log 2>&1
```

c) update_status_panel_ssh_server.py<br>
b.1) Adjust your user and script path following sample below
```bash
*/5 * * * * /usr/bin/python /home/user/callhome_ssh_server/update_status_panel_ssh_server.py >> /tmp/update_status_panel_ssh_server.log 2>&1
```

<h1>TROUBLESHOOTING</h1><br>
<b>Test API communication with Atlassian</b><br>
Create incident, replace abde for you Component ID<br>

```bash
curl https://api.statuspage.io/v1/pages/{page_id}/incidents \
  -H "Authorization: OAuth {api_token}" \
  -X POST \
  -d "incident[name]=Teste Component" \
  -d "incident[status]=investigating" \
  -d "incident[body]=Testando componentes" \
  -d "incident[component_ids][]=abcdefghijklmnopqrstuvwxyz" \
  -d "incident[component_ids][]=zyxwvutsrqponmlkjihgfedcba" \
  -d "incident[components][abcdefghijklmnopqrstuvwxyz]=major_outage" \
  -d "incident[components][zyxwvutsrqponmlkjihgfedcba]=major_outage"
```

<b>SAMPLE SIMPLE CURL</b><br>
<b>Test API communication with Cloudflare</b>b<br>

```bash
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
     -H "Authorization: Bearer abcdefghijklmnopqrstuvwxyz" \
     -H "Content-Type:application/json"
```

Remember to replace values between brackets for your correspondinds IDs/APIs.

```bash
abcdefghijklmnopqrstuvwxyz/zyxwvutsrqponmlkjihgfedcba 
```


