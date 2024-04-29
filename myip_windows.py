import subprocess
import re
from sendmail import send_mail_my_ip_is, send_mail_vpn_failed

def get_ipv4_from_ipconfig():
    try:
        # Run the ipconfig command
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
        output = result.stdout

        # Use regex to find the IPv4 address with pattern beginning with 192.168.113
        match = re.search(r'\.\s+\.\s+:\s+(192\.168\.113\.\d+)', output, re.IGNORECASE)

        if match:
            return match.group(1)  # Return the IPv4 address
        else:
            return None  # Return None if no IPv4 address found
    except Exception as e:
        print("Error:", e)
        return None
    
# Call the function to get the IPv4 address
myIpAddress = get_ipv4_from_ipconfig()

if myIpAddress:
    print("IPv4 Address is: ", myIpAddress)
    send_mail_my_ip_is(myIpAddress)

     # Write the IP address to a file
    with open('myIpAddress.txt', 'w') as f:
        f.write(myIpAddress)
else:
    print("No IPv4 address found for tun interface.")
    send_mail_vpn_failed()
