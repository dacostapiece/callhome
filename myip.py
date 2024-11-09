import subprocess
import re
from sendmail import send_mail_my_ip_is, send_mail_vpn_failed
import sys
import ipaddress
from writeandreadip_tunip import writeip
from config import myip_logfile

LOG_FILE = myip_logfile

def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")

#get isolated tun0 interface ip address
def get_tun_ipv4_from_ifconfig():
    try:
        # Run the ifconfig command
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
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

#get isolated eth interface ip address
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

#get isolated wlan interface ip address
def get_wlan_ipv4_from_ifconfig():
    try:
        # Run the ifconfig command
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        output = result.stdout

        # Use regex to find the "tun" interface and its associated IPv4 address
        match = re.search(r'(wlan\d+).*?inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,4})', output, re.DOTALL)

        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4  # Return the interface name and IPv4 address
        else:
            return None, None  # Return None if no IPv4 address found for "tun" interface
    except Exception as e:
        print("Error:", e)
        return None, None

#GET CURRENT IP ADDRESS with IP SHOW
def get_interfaces_ipv4_from_ifconfig():
    try:
        # Run the Linux command to get all interface information
        result = subprocess.run(["ip", "addr", "show"], capture_output=True, text=True, check=True)
        output = result.stdout

        if output:
            # Save response to a file
            with open("ipadd.txt", "w") as file:
                file.write(output)
            print("Current IP addresses stored to ipadd.txt")
            return output  # Return IP address information
        else:
            print("No IP addresses found.")
            return None  # Return None if no output from command
    except subprocess.CalledProcessError as e:
        print(f"Error: Command 'ip addr show' returned non-zero exit status {e.returncode}")
        return None  # Return None on command error
    except Exception as e:
        print("Error:", e)
        return None  # Return None on any other exception

# Call the function to get the interface name and IPv4 address associated with "tun" interface
def setVariables():
    interface, myIpAddress = get_tun_ipv4_from_ifconfig()
    interfaceETH, myIpAddressETH = get_eth_ipv4_from_ifconfig()
    interfaceWLAN, myIpAddressWLAN = get_wlan_ipv4_from_ifconfig()
    ifconfig_run = get_interfaces_ipv4_from_ifconfig()
    return interface, myIpAddress, interfaceETH, myIpAddressETH, interfaceWLAN, myIpAddressWLAN, ifconfig_run

def runMyIpAddres():
    interface, myIpAddress, interfaceETH, myIpAddressETH, interfaceWLAN, myIpAddressWLAN, ifconfig_run = setVariables()
    if myIpAddress:
        print("IPv4 Address for", interface, "interface:", myIpAddress)
        print("IPv4 Address for", interfaceETH, "interface:", myIpAddressETH)
        print("IPv4 Address for", interfaceWLAN, "interface:", myIpAddressWLAN)
        print("\n")
        print("Full Ifconfig below:")
        #print(ifconfig_run)
        send_mail_my_ip_is(myIpAddress,ifconfig_run, myIpAddressETH, myIpAddressWLAN)
        writeip(myIpAddress)
        print("Write IP: ", myIpAddress)
        log_message("myIpAddress (success)")

    else:
        print("No IPv4 address found for tun interface.")
        send_mail_vpn_failed()
        log_message("Exiting with code 2 (failure)")
        sys.exit(2) #Fail
    
if __name__ == "__main__":
    runMyIpAddres()