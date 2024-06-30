#!/usr/bin/env python3
import subprocess
import os
import sys
import socket
import time
import re
import logging

from config import ssh_username, ssh_server, ssh_options, check_status_string, check_interval

# Configure logging
logging.basicConfig(filename='/tmp/autossh_script_nivel2.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define the status string to check (adjust for different languages/environment)
check_status_string # Change as needed for different languages/environment

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

def restart_autossh():
    """ Restart autossh process. """
    try:
        subprocess.run(["pkill", "autossh"], check=True)
        logging.info("Stopped existing autossh process.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to stop autossh: {e}")

    try:
        command = f'autossh {ssh_options} {ssh_username}@{ssh_username}'
        subprocess.Popen(command, shell=True)
        logging.info("Started autossh process.")
    except Exception as e:
        logging.error(f"Failed to start autossh: {e}")

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
        print(f"Error resolving DNS for {hostname}: {e}")
        log_error(f"Error resolving DNS for {hostname}: {e}")
        sys.exit(2)

def start_autossh(command, log_file):
    """ Start autossh process and redirect output to log file. """
    try:
        with open(log_file, 'a') as log:
            # Start autossh process in the background, redirecting both stdout and stderr to log file
            subprocess.Popen(command, shell=True, stdout=log, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred starting autossh: {e}")
        log_error(f"An error occurred starting autossh: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"Error starting autossh: {str(e)}")
        log_error(f"Error starting autossh: {str(e)}")
        sys.exit(2)

def check_ssh_tunnel(ip_address, log_file, status_string):
    """ Check if SSH tunnel to IP address is established using netstat. """
    try:
        time.sleep(5)  # Wait for some time to allow the tunnel to establish

        # Check if SSH connection is established using netstat
        netstat_output = subprocess.check_output(['netstat', '-an', '--tcp']).decode()

        # Search for established SSH connection to ip_address:22 with the given status_string
        if re.search(rf'{re.escape(ip_address)}:22\s+{status_string}', netstat_output):
            print(f"SSH tunnel to {ip_address}:22 is established.")
            log_error(f"SSH tunnel to {ip_address}:22 is established.")
        else:
            print(f"SSH tunnel to {ip_address}:22 is not established.")
            print("\ncheck_ssh_tunnel loop - else")
            log_error(f"SSH tunnel to {ip_address}:22 is not established.")
            sys.exit(2)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during netstat check: {e}")
        log_error(f"An error occurred during netstat check: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"Error occurred during SSH tunnel check: {str(e)}")
        log_error(f"Error occurred during SSH tunnel check: {str(e)}")
        sys.exit(2)

def log_error(message):
    """ Log error message to log file. """
    log_file = '/tmp/autossh_script.log'
    with open(log_file, 'a') as log:
        log.write(f"Error: {message}\n")

# Main script logic
if __name__ == "__main__":
    # Resolve DNS to get SSH server IP address
    ssh_server_ip = resolve_dns(ssh_server)

    # Construct the autossh command
    autossh_command = f'autossh {ssh_options} {ssh_username}@{ssh_server}'

    # Open the log file for writing (append mode to keep all output)
    log_file = '/tmp/autossh_script.log'

     # Check if the SSH server is reachable before starting autossh
    if is_ssh_tunnel_active(ssh_server_ip, 22):
        print(f"SSH server {ssh_server_ip} is reachable.")
        logging.info(f"SSH server {ssh_server_ip} is reachable.")

        # Start autossh process
        start_autossh(autossh_command, log_file)

        # Check SSH tunnel status
        check_ssh_tunnel(ssh_server_ip, log_file, check_status_string)
    else:
        print(f"SSH server {ssh_server_ip} is not reachable.")
        logging.error(f"SSH server {ssh_server_ip} is not reachable.")
        sys.exit(1)




