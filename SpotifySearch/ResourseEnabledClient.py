import datetime
import base64
import requests
from urllib.parse import urlencode
from pprint import pprint

Client_ID = "Client_ID"
Secret_Key = "Secret_Key"

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    access_token_did_expire = None


    def __init__(self,client_id,client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must provide the client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_base64 = base64.b64encode(client_creds.encode())
        return client_creds_base64.decode()

    def get_token_header(self):
        client_creds_base64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_base64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client!")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        self.access_token = access_token
        print("Auth successful")
        return True

    def get_access_token(self):
        auth_done = self.perform_auth()
        if not auth_done:
            print("Authentication failed")
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        return token

    def search(self, query, search_type="track"):
        headers = self.get_resourse_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = {"q": query, "type": search_type}
        data_encode = urlencode(data)
        url_to_search = f"{endpoint}?{data_encode}"
        r = requests.get(url_to_search, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()

    def get_resourse_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type="albums", version="v1"):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resourse_header()
        print(headers)
        r = requests.get(endpoint, headers=headers)
        print(r.status_code)
        # if r.status_code not in range(200, 299):
        #     return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(lookup_id=_id, resource_type="albums")

    def get_artist(self, _id):
        return self.get_resource(lookup_id=_id, resource_type="artists")
