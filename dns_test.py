#!/usr/bin/env python3
import socket
import subprocess

def test_dns_resolution(hostname='www.google.com'):
    try:
        # Use the socket library to test DNS resolution with system's DNS settings
        result = socket.gethostbyname(hostname)
        print(f"DNS resolution successful: {hostname} -> {result}")
        return True
    except Exception as e:
        print(f"DNS resolution failed: {e}")
        return False

def call_alternative_script(script_path='/home/dacosta/CALLHOME/fixnameservers.sh'):
    try:
        # Call the alternative shell script using subprocess
        result = subprocess.run(['sh', script_path], capture_output=True, text=True)
        print(f"Alternative script output:\n{result.stdout}")
        print(f"Alternative script errors:\n{result.stderr}")
    except Exception as e:
        print(f"Failed to call the alternative script: {e}")

# def call_myip_script(script_path='/home/dacosta/CALLHOME/myip.py'):
#     try:
#         # Call the alternative shell script using subprocess
#         result = subprocess.run(['py', script_path], capture_output=True, text=True)
#         print(f"myip script output:\n{result.stdout}")
#         print(f"myip script errors:\n{result.stderr}")
#     except Exception as e:
#         print(f"Failed to call myip script: {e}")


if __name__ == "__main__":
    if not test_dns_resolution():
        call_alternative_script()
        # call_myip_script()
