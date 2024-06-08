import requests
from datetime import datetime
from config import api_token, page_id, name_create_incident, status_create_incident, impact_create_incident, monitoring_at_create_incident, body_create_incident

name = name_create_incident
status = status_create_incident
impact = impact_create_incident
monitoring_at = monitoring_at_create_incident
body = body_create_incident

url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents"
headers = {
    "Authorization": f"OAuth {api_token}"
}
data = {
    "incident[name]": name,
    "incident[status]": status,
    "incident[impact]": impact,
    "incident[monitoring_at]": monitoring_at,
    "incident[body]": body
}
response = requests.post(url, headers=headers, data=data)
# return_response = requests.post(url, headers=headers, json=data)

# Save response to a file
with open("create_incident_response.txt", "w") as file:
    file.write(response.text)

print("An incident has been created.")
print("Response saved to create_incident_response.txt")
response_data = response.json()
incident_id = response_data.get('id', None)