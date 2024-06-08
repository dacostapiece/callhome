from datetime import datetime
#
# Mail settings
mailserver = 'smtp.gmail.com'
smtpport = 587
mailusername = 'dacostapiecealerts@gmail.com'
mailpassword = 'bknd izkv zbhr jogq'
source_mailaddress = 'dacostapiecealerts@gmail.com'
dest_mailaddress = 'dacostapiecealerts@gmail.com'
mailsubject_success = "MY RASP TUN IP SERVICE ADDRESS IS: "
mailsubject_failed = "VPN Failed"

# Remote VPN Target
vpn_probe_target = "10.0.10.1"

#API General Settings
api_token = "2a93dea3212543298c99b5216b0e5e12"
page_id = "qb7hs0ds4l0d"

#API Create Incident
name_create_incident = "VPN com falha"
status_create_incident = "investigating"
impact_create_incident = "major"
monitoring_at_create_incident = f"Falha registrada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
body_create_incident = "VPN com falha, investigando"
deliver_notifications_create_incident = True
qxkt2r25bgrk = "major outrage"
components = {"qxkt2r25bgrk": "major outrage"}
component_ids = ["qxkt2r25bgrk"]

#API Update Incident
name_update_incident = "VPN restabelecida"
status_update_incident = "resolved"
updated_at_update_incident = f"Falha resolvida em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
body_update_incident = "VPN restabelecida"

