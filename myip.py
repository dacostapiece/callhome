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

# Call the function to get the interface name and IPv4 address associated with "tun" interface
interface, myIpAddress = get_tun_ipv4_from_ifconfig()

if myIpAddress:
    print("IPv4 Address for", interface, "interface:", myIpAddress)
    send_mail_my_ip_is(myIpAddress)
    log_message("Exiting with code 0 (success)")
    sys.exit(0) #Sucess

else:
    print("No IPv4 address found for tun interface.")
    send_mail_vpn_failed()
    log_message("Exiting with code 2 (failure)")
    sys.exit(2) #Fail
    
