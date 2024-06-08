import requests
import json


def update_incident(api_token, page_id, incident_id, name, status, updated_at, body):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/{incident_id}"
    headers = {
        "Authorization": api_token
    }
    data = {
        "incident[name]": name,
        "incident[status]": status,
        "incident[updated_at]": updated_at,
        "incident[body]": body
    }
    response = requests.patch(url, headers=headers, data=data)

    # Save response to a file
    with open("update_incident.txt", "w") as file:
        file.write(response.text)

    print("Incident updated. Response saved to update_incident.txt")
    response_data = response.json()
    solved_incident_id = response_data.get('id', None)
    return solved_incident_id