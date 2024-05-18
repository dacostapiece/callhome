The idea is to called these scripts after a device connects to VPN Server to advertises its tun interface IP address over email.

FIXNAMESERVERS.SH<br>
fixnameservers.sh must run as root, therefore
sudo chown root:root fixnameservers.sh
sudo chmod 700 fixnameservers.sh
check permissions
ls -al fixnameservers.sh
expected result
-rwx------ 1 root root 194 mai 13 18:02 fixnameservers.sh
