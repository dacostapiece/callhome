import requests
import json
from config import api_token, page_id, name_update_incident, status_update_incident, updated_at_update_incident, body_update_incident
from check_incident_status import raw_list_incident

name = name_update_incident
status = status_update_incident
updated_at = updated_at_update_incident
body = body_update_incident

incident_id = raw_list_incident(api_token, page_id)

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
