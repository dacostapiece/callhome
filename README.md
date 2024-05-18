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

<b>OPENVPN_SCRIPT.SH</b><br>
Script run openvpn - passing creds already

<b>PASS.TXT</b><br>
OpenVPN Creds

<b>SENDMAIL.PY</b><br>
This script works as a module called by my.ip which will receive tun0 IP address for VPN and send it out as email
