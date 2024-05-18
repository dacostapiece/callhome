The idea is to called these scripts after a device connects to VPN Server to advertises its tun interface IP address over email.

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
OpenVPN Creds

<b>SENDMAIL.PY</b><br>
This script works as a module called by my.ip which will receive tun0 IP address for VPN and send it out as email

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




