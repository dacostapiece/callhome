import requests
from config import api_token, page_id

def chk_incident(api_token, page_id):
    url = f"https://api.statuspage.io/v1/pages/{page_id}/incidents/unresolved"
    headers = {
        "Authorization": api_token
    }
    response = requests.get(url, headers=headers)

    # Save response to a file
    with open("check_incident_status_response.txt", "w") as file:
        file.write(response.text)
        print("Response saved to check_incident_status_response.txt")
    return response

if __name__ == "__main__":
    chk_incident(api_token, page_id)
