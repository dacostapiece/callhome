#!/usr/bin/env python3
import subprocess
import sys
from sendmail import send_mail_my_ip_is_updated, send_mail_vpn_failed
from myip import interface, interfaceETH, interfaceWLAN, myIpAddress, myIpAddressETH, myIpAddressWLAN, ifconfig_run
import re

LOG_FILE = "/tmp/updated_interfaces.py.log"
IFCONFIG_FILE = "ifconfig.txt"

def sum_ascii_values(s):
    return sum(ord(char) for char in s)

def compare_ascii_sums(values1, values2):
    sum1 = sum(sum_ascii_values(value) for value in values1)
    sum2 = sum(sum_ascii_values(value) for value in values2)
    return sum1 == sum2

def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")

def read_ifconfig_stored():
    try:
        with open(IFCONFIG_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        log_message(f"{IFCONFIG_FILE} not found. Assuming this is the first run.")
        return ""

def send_mail_if_needed():
    send_mail_my_ip_is_updated(myIpAddress, ifconfig_run, myIpAddressETH, myIpAddressWLAN)
    log_message("Interfaces have changed. Email notification sent.")

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
    values1 = ["interface", myIpAddress, interfaceETH, myIpAddressETH, interfaceWLAN, myIpAddressWLAN]
    values2 = [interfaceStored, myIpAddressStored, interfaceETHStored, myIpAddressETHStored, interfaceWLANStored, myIpAddressWLANStored]

    comparison_result = compare_ascii_sums(values1, values2)

    if comparison_result != True:
        send_mail_if_needed()
    else:
        print("Sem alterações de IP nas placas mais importantes.")
        None
