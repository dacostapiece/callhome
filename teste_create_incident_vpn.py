import requests
from datetime import datetime
from config import api_token, page_id, name_create_incident, status_create_incident, impact_create_incident, monitoring_at_create_incident, body_create_incident

from datetime import datetime

deliver_notifications_create_incident = True
component_ids = ["qxkt2r25bgrk"]

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
    "incident[name]": "COMPONENT TEST",
    "incident[status]": status,
    "incident[impact]": impact,
    "incident[monitoring_at]": monitoring_at,
    "incident[body]": body,
    "incident[deliver_notifications]": deliver_notifications_create_incident,
    "incident[component_ids]": component_ids,
    "incident[impact_override]": "critical",
    "components[qxkt2r25bgrk]": "partial_outrage"
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

def update_component(api_token, page_id, component_ids):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/components/{component_ids}"
    headers = {
    "Authorization": f"OAuth {api_token}"
    }
    data = {
    "component[status]": "partial_outrage"
    }
    response = requests.post(url, headers=headers, data=data)
    # return_response = requests.post(url, headers=headers, json=data)

    # Save response to a file
    with open("create_component_incident_response.txt", "w") as file:
        file.write(response.text)

    print("Component was updated.")
    print("Response saved to create_component_incident_response.txt")
    response_data = response.json()
    component_id = response_data.get('id', None)
    return component_id

update_component(api_token, page_id, component_ids)