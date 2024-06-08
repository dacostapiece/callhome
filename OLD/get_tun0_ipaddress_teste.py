import subprocess
import re

def get_tun0_ip():
    try:
        # Run the Linux command to get the IP address of the tun0 interface
        output = subprocess.check_output(["ip", "addr", "show", "tun0"]).decode("utf-8")
        # Use regular expression to extract the IP address
        tun0_ip = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output).group(1)
        return tun0_ip
    except subprocess.CalledProcessError:
        print("Interface tun0 not found.")
        return None
