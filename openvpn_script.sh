#!/bin/bash
exec &>>/tmp/openvpn_script.log
sudo openvpn --config /home/dacosta/CALLHOME/hub.ovpn --auth-user-pass /home/dacosta/CALLHOME/pass.txt

