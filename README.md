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
