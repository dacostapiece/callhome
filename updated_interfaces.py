#!/usr/bin/env python3
import subprocess
import ipaddress
import sys
from sendmail import send_mail_my_ip_is_updated, send_mail_vpn_failed
import re

LOG_FILE = "/tmp/updated_interfaces.py.log"
IFCONFIG_FILE = "/home/dacosta/CALLHOME/ifconfig.txt"

#GET CURRENT TUN IP ADDRESS
def get_tun_ipv4_from_ifconfig():
    try:
        # Run the ifconfig command
        result = subprocess.run(['/usr/sbin/ifconfig'], capture_output=True, text=True, check=True)
        output = result.stdout

        # Use regex to find the "tun" interface and its associated IPv4 address
        match = re.search(r'(tun\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', output, re.DOTALL)

        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4  # Return the interface name and IPv4 address
        else:
            return None, None  # Return None if no IPv4 address found for "tun" interface
    except Exception as e:
        print("Error:", e)
        return None, None

#GET CURRENT ETH IP ADDRESS
def get_eth_ipv4_from_ifconfig():
    try:
        # Run the ifconfig command
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        output = result.stdout

        # Use regex to find the "tun" interface and its associated IPv4 address
        match = re.search(r'(eth\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', output, re.DOTALL)

        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4  # Return the interface name and IPv4 address
        else:
            return None, None  # Return None if no IPv4 address found for "tun" interface
    except Exception as e:
        print("Error:", e)
        return None, None

#GET CURRENT WLAN IP ADDRESS
def get_wlan_ipv4_from_ifconfig():
    try:
        # Run the ifconfig command
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        output = result.stdout

        # Use regex to find the "tun" interface and its associated IPv4 address
        match = re.search(r'(wlan\d+).*?inet (\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4})', output, re.DOTALL)

        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4  # Return the interface name and IPv4 address
        else:
            return None, None  # Return None if no IPv4 address found for "tun" interface
    except Exception as e:
        print("Error:", e)
        return None, None

#GET CURRENT IFCONFIG INFO
def get_interfaces_ipv4_from_ifconfig():
    try:
        # Run the ifconfig command
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        output = result.stdout

        if output!="":
            return output  # Return ifconfig run
        else:
            return None, None  # Return None ifconfig run
    except Exception as e:
        print("Error:", e)
        return None, None

#GET VARIABLES
interface, myIpAddress = get_tun_ipv4_from_ifconfig()
interfaceETH, myIpAddressETH = get_eth_ipv4_from_ifconfig()
interfaceWLAN, myIpAddressWLAN = get_wlan_ipv4_from_ifconfig()
ifconfig_run = get_interfaces_ipv4_from_ifconfig()

#SUM ASCII CHAR FOR LATER COMPARISON
def sum_ascii_values(s):
    return sum(ord(char) for char in s)

#RETURN ASCII CHAR COMPARISON
def compare_ascii_sums(currentNetworkInfo, storedNetworkInfo):
    sum1 = sum(sum_ascii_values(value) for value in currentNetworkInfo)
    sum2 = sum(sum_ascii_values(value) for value in storedNetworkInfo)
    return sum1 == sum2

#OUTPUT LOG MESSAGE
def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")

#READ STORED IFCONFIG INFO
def read_ifconfig_stored():
    try:
        with open(IFCONFIG_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        log_message(f"{IFCONFIG_FILE} not found. Assuming this is the first run.")
        return ""

#SEND MAIL IF IPs HAVE CHANGED
def send_mail_if_needed():
    #NETWORK INFO WILL BE PULLED FROM HERE FOR MAIL SENDING
    send_mail_my_ip_is_updated(myIpAddress, ifconfig_run, myIpAddressETH, myIpAddressWLAN)
    log_message("Interfaces have changed. Email notification sent.")

#READ STORED TUN INFO
def get_tun_ipv4_from_ifconfig_Stored(ifconfig_output):
    try:
        match = re.search(r'(tun\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_output, re.DOTALL)
        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4
        else:
            return None, None
    except Exception as e:
        log_message(f"Error parsing ifconfig output: {e}")
        return None, None

#READ STORED ETH0 INFO
def get_eth_ipv4_from_ifconfig_Stored(ifconfig_output):
    try:
        match = re.search(r'(eth\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_output, re.DOTALL)
        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4
        else:
            return None, None
    except Exception as e:
        log_message(f"Error parsing ifconfig output: {e}")
        return None, None
    
#READ STORED WLAN INFO
def get_wlan0_ipv4_from_ifconfig_Stored(ifconfig_output):
    try:
        match = re.search(r'(wlan\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ifconfig_output, re.DOTALL)
        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4
        else:
            return None, None
    except Exception as e:
        log_message(f"Error parsing ifconfig output: {e}")
        return None, None
    
#update ifconfig.txt to current interfaces info after comparison
def update_get_interfaces_ipv4_from_ifconfig():
    try:
        # Run the ifconfig command
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        output = result.stdout

        if output!="":
                        # Save response to a file
            with open("ifconfig.txt", "w") as file:
                file.write(output)
                print("Current ifconfig stored to ifconfig.txt")
            return output  # Return ifconfig run
        else:
            return None, None  # Return None ifconfig run
    except Exception as e:
        print("Error:", e)
        return None, None

#STARTS CHECKING NETWORK INFO FOR COMPARISON
if ifconfig_run is None:
    log_message("Failed to retrieve ifconfig output.")
    sys.exit(2)
else:
    ifconfig_stored = read_ifconfig_stored()

    # Call the function to get the interface name and IPv4 address associated with "tun" interface
    interfaceStored, myIpAddressStored = get_tun_ipv4_from_ifconfig_Stored(ifconfig_stored)
    interfaceETHStored, myIpAddressETHStored = get_eth_ipv4_from_ifconfig_Stored(ifconfig_stored)
    interfaceWLANStored, myIpAddressWLANStored = get_wlan0_ipv4_from_ifconfig_Stored(ifconfig_stored)

    # Call the function to get the interface name and IPv4 address associated with "tun" interface
    currentNetworkInfo = [interface, myIpAddress, interfaceETH, myIpAddressETH, interfaceWLAN, myIpAddressWLAN]
    storedNetworkInfo = [interfaceStored, myIpAddressStored, interfaceETHStored, myIpAddressETHStored, interfaceWLANStored, myIpAddressWLANStored]

    comparison_result = compare_ascii_sums(currentNetworkInfo, storedNetworkInfo)

    if comparison_result != True:
        send_mail_if_needed()
        #update_get_interfaces_ipv4_from_ifconfig()
    else:
        print("Sem alterações de IP nas placas mais importantes.")
        None