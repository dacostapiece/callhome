import requests
import ipaddress
import subprocess
import re

# Cloudflare API credentials
CF_API_TOKEN = 'Your Cloudflare API Token - see Read.me for more info'

# Cloudflare Zone ID and DNS record information
ZONE_ID = 'Your cloudflare zone id'
DNS_RECORD_NAME = 'the FQDN will want to update'
DNS_RECORD_ID = 'The ID for that FQDN - see Read.me for more info'

# Function to get the IP address from interface tun0
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


# Function to update DNS record in Cloudflare
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
        else:
            print("Failed to update DNS record.")
    else:
        print("Failed to fetch DNS record ID.")
        print(response.content)  # Print response content for debugging

def main():
    tun0_ip = get_tun0_ip()
    if tun0_ip:
        update_dns_record(tun0_ip)

if __name__ == "__main__":
    main()

#test API connection
# curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
#      -H "Authorization: [your API token]" \
#      -H "Content-Type:application/json"

# #sample command to update dns record in cURL
# curl --request PATCH \
#   --url https://api.cloudflare.com/client/v4/zones/[zone id]/dns_records/[record id] \
#   --header 'Content-Type: application/json' \
#   --header 'Authorization: Bearer [your API token]'\
#   --data '{
#   "content": "1.1.1.1",
#   "name": "[your FQDN]",
#   "proxied": false,
#   "type": "A",
#   "ttl": 120
# }'
