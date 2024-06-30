from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables from the .env file
load_dotenv()

# Mail settings
mailserver = os.getenv('mailserver')
smtpport = os.getenv('smtpport')
mailusername = os.getenv('mailusername')
mailpassword = os.getenv('mailpassword')
source_mailaddress = os.getenv('source_mailaddress')
dest_mailaddress = os.getenv('dest_mailaddress')
mailsubject_success = "MY RASP IP ADDRESSES ARE: "
mailsubject_success_updated = "MY UPDATED RASP IP ADDRESSES ARE: "
mailsubject_failed = "VPN Failed"

# Remote VPN Target
vpn_probe_target = os.getenv('vpn_probe_target')

#API General Settings - Status Panel
api_token = os.getenv('api_token')
page_id = os.getenv('page_id')

#API Create Incident - Status Panel
name_create_incident = "VPN com falha"
status_create_incident = "investigating"
impact_create_incident = "major"
monitoring_at_create_incident = f"Falha registrada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
body_create_incident = "VPN com falha, investigando"
deliver_notifications_create_incident = True
qxkt2r25bgrk = "major outrage"
components = {"qxkt2r25bgrk": "major outrage"}
component_ids = ["qxkt2r25bgrk"]

#API Update Incident - Status Panel
name_update_incident = "VPN restabelecida"
status_update_incident = "resolved"
updated_at_update_incident = f"Falha resolvida em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
body_update_incident = "VPN restabelecida"

# Cloudflare API credentials
CF_API_TOKEN = os.getenv('CF_API_TOKEN')

# Cloudflare Zone ID and DNS record information
ZONE_ID = os.getenv('ZONE_ID')
DNS_RECORD_NAME = os.getenv('DNS_RECORD_NAME')
DNS_RECORD_ID = os.getenv('DNS_RECORD_ID')

# Define your sensitive information as environment variables
ssh_username = os.getenv('SSH_USER')
ssh_server = os.getenv('SSH_SERVER')
ssh_options = os.getenv('SSH_OPTIONS')

check_status_string = 'ESTABELECIDA'  # Change as needed for different languages/environment
#check_status_string = 'established'  # Change as needed for different languages/environment
check_interval = 60

#SSH-AGENT Handling
key_file = os.getenv('KEY_FILE')
key_password = os.getenv('SSH_KEY_PASSWORD')