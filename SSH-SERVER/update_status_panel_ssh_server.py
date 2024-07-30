#!/usr/bin/env python3
from tunnel_connection import check_vpn_connection
from check_incident_status_ssh_server import list_incident, raw_list_incident
from config_ssh_server import api_token, page_id, name_create_incident, status_create_incident, impact_create_incident, monitoring_at_create_incident, body_create_incident, name_update_incident, status_update_incident, updated_at_update_incident, body_update_incident
from check_incident_status_ssh_server import create_incident
from update_incident_ssh_server import update_incident

def is_vpn_working():
    if check_vpn_connection()==True:
        print("Checking if there any current Incidents?")
        if list_incident(api_token, page_id)==False:
            print("VPN is working, No incidents found, OK!")
            return True
        else:
            current_incident_id = raw_list_incident(api_token, page_id)
            print("Current Incident ID: ", current_incident_id)
            print("VPN is working. Solving issue: ", current_incident_id)
            solved_incident_id = update_incident(api_token, page_id, current_incident_id, name_update_incident, status_update_incident, updated_at_update_incident, body_update_incident)
            return solved_incident_id
    else:
        print("Checking if there any current Incidents?")
        if list_incident(api_token, page_id)==False:
            current_incident_id = create_incident(api_token, page_id, name_create_incident, status_create_incident, impact_create_incident, monitoring_at_create_incident, body_create_incident)
            print("Created Incident ID: ", current_incident_id)
            return current_incident_id
        else:
            print("VPN is not working, But we´ve found register incident, OK!")
            current_incident_id = raw_list_incident(api_token, page_id)
            print("Ongoing Incident ID: ", current_incident_id)
            return True    

print("Checking VPN Status...")
status_vpn = is_vpn_working()