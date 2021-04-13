import requests
import base64
import datetime

Client_ID = "Client_ID"
Secret_Key = "Secret_Key"

method = "POST"
url_auth_endpoint = "https://accounts.spotify.com/api/token"

client_creds = f"{Client_ID}:{Secret_Key}"

client_creds_base64 = base64.b64encode(client_creds.encode())

token_data = {
    "grant_type": "client_credentials"
}

token_headers = {
    "Authorization": f"Basic {client_creds_base64.decode()}"
}

r = requests.post(url_auth_endpoint, data=token_data, headers=token_headers)
token_response_data = r.json()

valid_request = r.status_code in range(200,299)

if valid_request:
    token_response_data = r.json()
    now = datetime.datetime.now()
    access_token = token_response_data["access_token"]
    expires_in = token_response_data["expires_in"]
    expires = now + datetime.timedelta(seconds=expires_in)
    did_expire = expires < now
