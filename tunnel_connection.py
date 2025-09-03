import subprocess
import time
from config import vpn_probe_target, ssh_server, ssh_port, tunnelconnection_ssh
import re
import socket
import sys
import logging
import ping3
import ipaddress
from ping3 import ping, errors

#HUB VPN CHECK
def check_tun0_ip():
    try:
        # Check if tun0 interface has an IP address
        ip_check = subprocess.check_output(['ip', 'addr', 'show', 'tun0']).decode('utf-8')
        if 'inet ' in ip_check:
            return True
    except subprocess.CalledProcessError:
        pass
    return False

# def ping_ip(ip, timeout=60):
#     end_time = time.time() + timeout
#     while time.time() < end_time:
#         try:
#             # Ping the IP address
#             ping_check = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#             if ping_check.returncode == 0:
#                 return True
#         except subprocess.SubprocessError:
#             pass
#         time.sleep(1)
#     return False

def check_ip_address(ip):
    print("Passed IP value: ", ip)
    try:
        # Attempt to create an IPv4 or IPv6 address object
        ip_obj = ipaddress.ip_address(ip)
        
        # Determine if it's IPv4 or IPv6
        if isinstance(ip_obj, ipaddress.IPv4Address):
            print("Found IPv4: ", ip)
            return ip
        elif isinstance(ip_obj, ipaddress.IPv6Address):
            print("Found IPv6: ", ip)
            return ip
    except ValueError:
        print("Invalid IP address format olá")
        return False

#PING3
def ping_ip(ip, timeout=10):
    #ip = "172.16.113.4"
    try:
        # Ensure the IP is a valid string before passing to ping
        if not isinstance(ip, str) or not ip:
            raise ValueError(f"Invalid IP address: {ip}")
        
        ipcheck = check_ip_address(ip)
        #bogus teste below
        #ipcheck = "IPv4"

        if ipcheck == False:
            return False

        # Send ICMP request and get the response time
        print("\n")
        print("ping ip funcion")
        print("early")
        print("ip: ", ipcheck)
        print("RESPONSE TIME BROTHER")
        
        #pdb.set_trace()
        response_time="Starting Response Time"
        print("response_time: ", response_time)
        #RUNNING IS BREAKING HERE

        print("\n")
        response_time = ping(ipcheck, timeout=timeout)
        print("RESPONSE TIME SISTER")
        print("later")
        print("ip: ", ipcheck)
        print("response_time: ", response_time)
        print("response_time var type: ", type(response_time))

        if response_time is None or response_time is False:
            print(f"Ping to {ipcheck} failed. No response.")
            time.sleep(1)
            return False  # Return a proper boolean value
            #return "Falseano brow"  # I dont know why i was returning a string Phrase
        else:
            print(f"Ping to {ipcheck} successful. Response time: {response_time} seconds")
            return True

    except Exception as e:
        print(f"ICMP error occurred while pinging {ip}: {str(e)}")
        time.sleep(1)
        return False

    except ValueError as ve:
        print("ValueError")
        print(str(ve))
        return False

def check_vpn_connection():
    if check_tun0_ip():
        if ping_ip(vpn_probe_target):
            print("Remote probe ", vpn_probe_target, " is responding!")
            return True
        else:
            print("Dev tun0 has IP address, but remote target isn't replying")
            return False
    else:
        print("Dev tun0 doesnt exist - OpenVPN is not working at all")
        return False

#SSH SERVER CHECK    
def resolve_dns(hostname):
    """ Resolve DNS hostname to IP address or return if already an IP address. """
    # Regular expression to match IPv4 addresses
    ipv4_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    
    # Check if the hostname is an IPv4 address
    if ipv4_pattern.match(hostname):
        return hostname  # Return the IPv4 address as is
    
    # If not an IPv4 address, resolve the DNS hostname to an IP address
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror as e:
        print(f"Error resolving DNS in tunnel_connection for {hostname}: {e}")
        logging.error(f"Error resolving DNS in tunnel_connection for {hostname}: {e}")
        sys.exit(2)

def is_ssh_tunnel_active(host, port):
    """ Check if the SSH tunnel is active by attempting a connection. """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except socket.error:
        return False
    finally:
        s.close()

def check_ssh_connection():
    # Resolve DNS to get SSH server IP address
    ssh_server_ip = resolve_dns(ssh_server)

    # Open the log file for writing (append mode to keep all output)
    log_file = tunnelconnection_ssh

     # Check if the SSH server is reachable before starting autossh
    if is_ssh_tunnel_active(ssh_server_ip, ssh_port)==True:
        print(f"SSH server {ssh_server_ip} is reachable.")
        logging.info(f"SSH server {ssh_server_ip} is reachable.")
        return True
    else:
        print("SSH Server is not port responding")
        return False
