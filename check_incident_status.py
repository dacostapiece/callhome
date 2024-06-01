import requests
from config import api_token, page_id

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

    # Check for the incident ID
    incident_id = response_data[0].get('id', None) if response_data else None
    if incident_id is None:
        print("No unresolved incidents found.")
        return False
    else:
        #print(f"Current Incident ID: {incident_id}")
        return incident_id

def raw_list_incident(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    incident_id = response_data[0].get('id', None) if response_data else None
    return incident_id