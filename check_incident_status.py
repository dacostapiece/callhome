import requests
from config import raspberry_vpn_component_id, remote_ssh_server_component_id

#HUB VPN INCIDENT
def list_incident(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    # Save response to a file
    with open("check_incident_status_response.txt", "w") as file:
        file.write(response.text)
        print("Response saved to check_incident_status_response.txt")

    if not response_data:
        print("No incidents found.")
        return False
    
    # Extract incident ID and component IDs
    incident_id = response_data[0].get('id', None) if response_data else None
    component_ids = [component.get('id') for component in response_data[0].get('components', [])]

    if component_ids:
        component_ids_isolated = component_ids[0]
    else:
        component_ids_isolated=None

    pair_incident = [incident_id, component_ids_isolated]

    # Checking
    if pair_incident is None:
        print("No unresolved incidents found.")
        return False
    else:
        #Is this incident related to Rasp VPN?
        print("Is this incident related to Rasp VPN?")
        if pair_incident[1]==raspberry_vpn_component_id:
            print("it's VPN related")
            return pair_incident
        else:
            print("No unresolved incidents found for Rasp VPN.")
            print("Any other incidents? ", pair_incident[0])
            return False

def raw_list_incident(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    #Extract incident ID and component IDs
    incident_id = response_data[0].get('id', None) if response_data else None
    component_ids = [component.get('id') for component in response_data[0].get('components', [])]

    if component_ids:
        component_ids_isolated = component_ids[0]
    else:
        component_ids_isolated=None

    pair_incident = [incident_id, component_ids_isolated]
    #Is this incident related to Rasp VPN?
    print("Is this incident related to Rasp VPN?")
    if pair_incident[1]==raspberry_vpn_component_id:
        print("it's VPN related")
        return pair_incident[0]
    else:
        print("No unresolved incidents found for Rasp VPN.")
        return None
    
    #SSH SERVER INCIDENT
def list_incident_ssh(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    # Save response to a file
    with open("check_incident_status_response_ssh.txt", "w") as file:
        file.write(response.text)
        print("Response saved to check_incident_status_response_ssh.txt")

    if not response_data:
        print("No incidents found.")
        return False
    
    # Extract incident ID and component IDs
    incident_id = response_data[0].get('id', None) if response_data else None
    component_ids = [component.get('id') for component in response_data[0].get('components', [])]

    if component_ids:
        component_ids_isolated = component_ids[0]
    else:
        component_ids_isolated=None

    pair_incident = [incident_id, component_ids_isolated]

    # Checking
    if pair_incident is None:
        print("No unresolved incidents found.")
        return False
    else:
        #Is this incident related to Rasp VPN?
        print("Is this incident related to Rasp VPN?")
        if pair_incident[1]==remote_ssh_server_component_id:
            print("it's SSH Server related")
            return pair_incident
        else:
            print("No unresolved incidents found for Remote SSH Server.")
            print("Any other incidents? ", pair_incident[0])
            return False

def raw_list_incident_ssh(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    #Extract incident ID and component IDs
    incident_id = response_data[0].get('id', None) if response_data else None
    component_ids = [component.get('id') for component in response_data[0].get('components', [])]

    if component_ids:
        component_ids_isolated = component_ids[0]
    else:
        component_ids_isolated=None

    pair_incident = [incident_id, component_ids_isolated]
    #Is this incident related to Rasp VPN?
    print("Is this incident related to Rasp VPN?")
    if pair_incident[1]==remote_ssh_server_component_id:
        print("it's SSH Server related")
        return pair_incident[0]
    else:
        print("No unresolved incidents found for Remote SSH Server.")
        return None