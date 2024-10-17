<b>RFE</b><br>
1) Enable hotspot if no LAN or WLAN is unavailable (No known WLAN creds and/or range reachable)<br>
2) Handle multiple interfaces from single type - two VPNs, more than one ETH, etc...
3) Start Webserver to receive SSID and password creds to login to neighbouring SSID
4) Clean code
5) Iterate loop only on associated components IDs - VPN Checks VPNs Incidents related, SSH  Checks SSH Incidents related, and so on.
6) Improve SSH habdling in SSH External Server - handle stale processes
7) Create a Install script

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
<h1>STEPS TO SETUP THIS PROJECT IN YOUR ENVIRONMENT</h1>

```bash
1) Get you API Token ID from in your Cloudflare account with associated FQDN domain
a) Go to:
https://dash.cloudflare.com/profile/api-tokens/
b) Select Create Token in API Tokens
c) Choose Edit Zone DNS and click on Use Template
d) Choose permissions Zone/DNS/Edit
e) Choose resources Include/Specific zone/example.com
f) Continue to summary
g) Create Token
h) Copy token

https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids
https://developers.cloudflare.com/fundamentals/api/get-started/create-token
https://dash.cloudflare.com/profile/api-tokens

2) Get your DNS Zone ID in your Cloudflare account with associated FQDN domain
a) Log into your Cloudflare account
b) Go to Websites/example.com
c) On far right you'll see your Zone ID record

3) Create three DNS Type A records without DNS proxy and TTL 5min in your Cloudflare account with associated FQDN domain.
a) raspberry.example.com for VPN Tunnel Raspberry IP device
You can set whatever IPv4 address, just for sake of creation of this DNS record
After create, we'll edit it just to create an audit log for later purpose
b) server.example.com for External SSH device
Set External SSH Server Public IP address for this DNS record
<b>Note:</b> You can create and associate a FQDN for you External SSH Server Public IP address or use an existing FQDN for it
c) hub.example.com for VPN Server
Set VPN Server Public IP address for this DNS record
<b>Note:</b> You can create and associate a FQDN for you VPN Server Public IP address or use an existing FQDN for it
d) Log into your Cloudflare account
e) On left sidebar menu, go to Manage account/Audit log
f) Expand recent audit logs for DNS changes and grab DNS record ID for raspberry.example.com.
The DNS record ID will be simply called "id"
Example
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
https://community.cloudflare.com/t/cannot-find-record-id/326344
Don't misundertook zone id with dns record id
4) You can use any SMTP Server to sending our own E-mail notifications. In our scenario we're going to an Gmail account
a) Create a new or login to your existing Gmail account
b) After validation or creation of new Gmail account, go to
https://myaccount.google.com/apppasswords
c) Give it a name and click on create
d) The generated app password will popup to you, this password will be used in our script to authenticate and send e-mails using our Gmail account
e) You can always go back to same link and delete the password app if desired.

5) Setting up your Status Page panel from Atlassian
a) Go to https://www.atlassian.com/software/statuspage
b) Create your free account
c) Choose subdomain name in your Atlassian account
Example
examplepanel.atlassian.net
Click next if possible, THIS IS NOT you Status Panel page, it's something else under the Umbrella of Atlassian/Jira cloud services
d) It may be requested (currently it's for new accounts) a component creation in a setup wizard
We're going to need four components, here they are:

<b>OpenVPN Outbound Raspberry Device</b>
Description: The primary VPN connection from Raspberry device to HUB VPN Gateway

<b>SSH Tunnel Outbound Raspberry Device</b>
Description:The secondary VPN connection over SSH Tunnel from Raspberry device to External SSH Server.

<b>External OpenVPN Raspberry Device Check</b>
Description: This component checks externally from SSH Server if VPN connection to Raspberry is working. It will connect to same VPN HUB device and try pinging Raspberry current tunnel IP address.

<b>External SSH Tunnel Raspberry Device Check</b>
Description: This component checks externally from SSH Server if the callback SSH Tunnel connection to Raspberry is working. It will try to connect to Raspberry SSH Service.

If requested, you don't need to setup a Component group. You can leave as it is or play with it later on as pleased. This project doesn't use Component group.

If Components wouldn't be requested at the new account startup, you'll need to setup them later.

e) In the current situation, after four components were added, just click Next
f) Upload a Status Panel image logo or click Next, you can add it later on
g) Setup e-mail to receive UPs and Downs regarding your components/services - click Send test email
For me it didn't workout sending out a test email through Atlassian new account wizard. When i first used Status Page, i added manually on own.
While writing this doc, i've just realized admin notification from Atlassian Status Panel it seems to have two different approaches.
g.1) Remind admins of ongoing incident - standard every 3, 6, 12 and 24 hours - this notification will be sent to e-mail account associated to your Atlassian account
g.2) For our project and to receive at the moment incident notification from Atlassian, you have to subsbribe it. You can choose whatever e-mail account you might like receiving those email notifications. We suggest you use the recent created Gmail account or any e-mail address that it's supposed to receive those notifications
g.3) Subscribing to your own Status Panel, click on View status page
g.4) In our example, it opens up page: https://examplepanel.statuspage.io/
g.5) Select Subscribe to Updates
g.6) Enter your e-mail address - i haven't tested other subscription options like x.com - you can try it later
g.7) Go to your e-mail account, open up Confirm you subscription mail message and click on Confirm
g.8) You'll be redirected to Status Panel page with an advise that confirmation was sucessful
g.9) There you go, anytime an incident occurs or get its clear, you'll receive an e-mail message.

6) Get your API Token and Page ID for Atlassian Status Panel
a) Go to Upper right "power" button and click it for change Settings
b) Select API info
c) Create key - give it a name - you call it whatever you like, i suggest "Callhome"
d) Take note of your API Key for Atlassian Status Panel
e) On same page you'll have down below the page next to Page IDs, your Page ID, take a note of it

h) Invite a team member - it suggests you to do it, i haven't done. I'll suggest you to skip it for now, click Next.
i) Save and exit to conclude Wizard
j) On Status Page, click on Activate your page and select FREE plan, confirm role based warning telling you Free plan doesn't - we wont need it

4) Clone and/or download this repository (callhome) under desired folder in your local linux device, here in our example, a raspberry device.
If downloaded, remember unzip its folder
a) Take note of the complete full path from this repository - you can call "pwd" inside the directory to get its full path location

6) Setup SSH Settings for Remote Access IN Raspberry
a) For Raspberry, the most easy is
b) Access it over GUI in virtual machine/HDMI monitor
c) Click on Raspberry icon upper left/Preferences
d) Click on Raspberry PI Configuration
e) On Interfaces tab, toggle ON for SSH
IF Available On Interfaces tab, toggle ON for VNC for remote GUI access
IF VNC option doesnt show, google it how to enable VNC or if you dont want, just ignore VNC step
f) SSH user and password creds are the same you setup (or standard?) for raspberry device
```

IF YOUR LOCAL DEVICE is not a Raspberry PI, here an example to setup SSH Server for Kali Linux.<br> 
If SSH isn't already enable on your local device, please google it how to enable it<br>

```bash
sudo apt-get update
sudo apt-get install ssh
sudo systemctl enable ssh
sudo service ssh start
```

7) Setup SSH Settings for External SSH Server<br>
Jump to this topic on Callhome SSH Server repository readme.md<br> 
https://github.com/dacostapiece/callhome_ssh_server<br>

8) Setup SSH Keys for SSH Reverse Tunnel between Raspberry and External SSH Server
a) Call ssh key generator
b) Enter file name with full path or hit enter to maintain default
If you type a desired name for ssh key pair, but you don't specify full path directory, key pair will be saved on the current directory
You can type "pwd" to check current full path directory
c) Enter SSH key password, you hit enter, no password will be set, for sake of current project, please set a password and take note
d) Repeat password if it was entered before
Key with .pub - public key
Key without extension - private key


```bash
a)
ssh-keygen -t ed25519
#ed25519 or preferable encryption algorihtm for SSH Key
```

9) Shared SSH public key to External SSH Server
Do it once you already have setup and SSH creds for External SSH Server
```bash
ssh-copy-id -i /path/to/custom_key.pub username@remote_server
```
If ssh-copy-id is unavailable, cat your file.pub (SSH Key public key) content and save it at on External SSH Server<br>
/home/user/.ssh/authorized_keys
If this file doesn't exist, create it on External SSH Server
You can test this authentication
a) Enable SSH Agent with Environment Variable
b) Add desired PRIVATE KEY file here exampled by "keyfile"
c) Enter password if the SSH Key was password encrypted
d) Try SSH into External SSH Server passing the private key already (From SSH-Agent)
```bash
eval "$(ssh-agent -s)"
ssh-add /home/user/.ssh/keyfile
ssh kali@server.example.com
```

```bash
7) atlassian
8) gmail
9) create an .env file using template below inside your download repository folder
```

<b>.ENV file template</b><br>
```bash
#.env

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
ZONE_ID = 'your just found DNS zone ID for the domain you're using it'
DNS_RECORD_NAME = 'raspberry.example.com'
DNS_RECORD_ID = 'your just found DNS record ID for the raspberry fqdn domain name you'll use it for raspberry'

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

<b>SAMPLE SIMPLE CURL</b><br>
<b>So you can test API communication with Cloudflare</b>b<br>

```bash

curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
     -H "Authorization: Bearer {Cloudflare API Token}" \
     -H "Content-Type:application/json"
```
Remember to replace values between brackets { } for your correspondinds IDs.
