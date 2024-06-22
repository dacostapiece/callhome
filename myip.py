import subprocess
import re
from sendmail import send_mail_my_ip_is, send_mail_vpn_failed
import sys

LOG_FILE = "/tmp/myip.py.log"

def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")

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
        match = re.search(r'(wlan\d+).*?inet (\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4})', output, re.DOTALL)

        if match:
            interface, ipv4 = match.group(1), match.group(2)
            return interface, ipv4  # Return the interface name and IPv4 address
        else:
            return None, None  # Return None if no IPv4 address found for "tun" interface
    except Exception as e:
        print("Error:", e)
        return None, None

#get other interfaces info
def get_interfaces_ipv4_from_ifconfig():
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
        print("\n")
        print("Full Ifconfig below:")
        print(ifconfig_run)
        send_mail_my_ip_is(myIpAddress,ifconfig_run, myIpAddressETH, myIpAddressWLAN)
        log_message("myIpAddress (success)")

    else:
        print("No IPv4 address found for tun interface.")
        send_mail_vpn_failed()
        log_message("Exiting with code 2 (failure)")
        sys.exit(2) #Fail
    
if __name__ == "__main__":
    runMyIpAddres()