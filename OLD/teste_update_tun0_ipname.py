import requests
import subprocess
import re
from datetime import datetime
import json

# Cloudflare API credentials
CF_API_TOKEN = 'Qv5b8bePRqrJNti0qifoPzLJpyq4NxZD1-nO4xaq'

# Cloudflare Zone ID and DNS record information
ZONE_ID = '615bfd2ecd68639dab792dbc57a2bdca'
DNS_RECORD_NAME = 'vpn.dacostapiece.com.br'
DNS_RECORD_ID = '573460b3c4763fd9b1ca81a7ce01a4d1'

LOG_FILE_PATH = "/tmp/update_tun0_ipname.log"
API_RESPONSE_FILE = "update_tun0_ipname_response.txt"

def log_run_time():
    """Logs the date and time the script was run to the log file."""
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write("\n")
        log_file.write(f"Script run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

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

def update_dns_record(ip):
    headers = {
        'Authorization': f'Bearer {CF_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records'
    params = {
        'type': 'A',
        'name': DNS_RECORD_NAME
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    with open(API_RESPONSE_FILE, 'w') as response_file:
        response_file.write(json.dumps(data))  # Save API response to a file
    if response.status_code == 200 and data['success']:
        record_id = data['result'][0]['id']
        update_url = f'{url}/{record_id}'
        payload = {
            'type': 'A',
            'name': DNS_RECORD_NAME,
            'id': record_id,
            'content': ip,
            'ttl': 120,  # Adjust TTL as needed
            'proxied': False  # Adjust proxy settings as needed
        }
        response = requests.put(update_url, headers=headers, json=payload)
        if response.status_code == 200 and response.json()['success']:
            print(f"DNS record {DNS_RECORD_NAME} updated successfully with IP address {ip}.")
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write(f"DNS record {DNS_RECORD_NAME} updated successfully with IP address {ip}.\n")
        else:
            print("Failed to update DNS record.")
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write(f"Failed to update DNS record.\n")
    else:
        print("Failed to fetch DNS record ID.")
        print(response.content)  # Print response content for debugging
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(f"Failed to fetch DNS record ID.\n")

def main():
    tun0_ip = "1.1.1.1"
    log_run_time()
    if tun0_ip:
        update_dns_record(tun0_ip)

if __name__ == "__main__":
    main()
