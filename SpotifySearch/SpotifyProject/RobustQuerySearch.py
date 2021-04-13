import datetime
import base64
import requests
from urllib.parse import urlencode
from pprint import pprint
import json
import webbrowser


Client_ID = "Client_ID"
Secret_Key = "Secret_Key"
Redirect_uri = "Redirect_uri"

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    client_id = None
    client_secret = None
    redirect_uri = None
    token_url = "https://accounts.spotify.com/api/token"
    access_token_did_expire = None
    access_OAth_2_token_expires = None
    access_OAth_2_token = None
    access_OAth_2_refresh_token = None
    user_id = None
    playlist_id = None


    def __init__(self,client_id,client_secret, redirect_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

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

    def get_OAth_2_token_data(self):
        return {
            "grant_type": "authorization_code"
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


    def perform_auth_code(self):
        self.get_OAuth_code()
        token_url = self.token_url
        redirect_uri = self.redirect_uri
        header = self.get_token_header()
        data = {
            "grant_type": "authorization_code",
            "code": str(input("Enter the code: ")),
            "redirect_uri": redirect_uri
        }
        r = requests.post(token_url, data=data, headers=header)
        data = r.json()
        now = datetime.datetime.now()
        refresh_token = data["refresh_token"]
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_OAth_2_token_expires = expires
        self.access_OAth_2_token = access_token
        self.access_OAth_2_refresh_token = refresh_token
        # print(access_token)
        # print(data)
        print("OAuth 2.0 successful")
        return True

    def get_OAuth_code(self):
        url_base = "https://accounts.spotify.com/authorize"
        client_id = self.client_id
        redirect_uri = self.redirect_uri
        data = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": "user-read-private user-read-email playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative",
        }
        url_endpoint = f"{url_base}?{urlencode(data)}"
        webbrowser.open_new_tab(url_endpoint)



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


    def base_search(self, query_params):
        headers = self.get_resourse_header()
        endpoint = "https://api.spotify.com/v1/search"
        url_to_search = f"{endpoint}?{query_params}"
        r = requests.get(url_to_search, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query=None, search_type="artist"):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        query = f"{query}"
        query_params = urlencode(({"q": query, "type": search_type.lower()}))
        return self.base_search(query_params)

    def get_resourse_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resourse_OAuth_2_header(self):
        self.perform_auth_code()
        access_token = self.access_OAth_2_token
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        url_endpoint = "https://api.spotify.com/v1/me"
        r = requests.get(url_endpoint, headers=headers)
        data = r.json()
        user_id = data["id"]
        self.user_id = user_id
        return headers

    def get_resource(self, lookup_id, resource_type="albums", version="v1"):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resourse_header()
        print(headers)
        r = requests.get(endpoint, headers=headers)
        print(r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(lookup_id=_id, resource_type="albums")

    def get_artist(self, _id):
        return self.get_resource(lookup_id=_id, resource_type="artists")

    def get_link(self, query=None, search_type="artist"):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        query = f"{query}"
        query_params = urlencode(({"q": query, "type": search_type.lower()}))
        content = self.base_search(query_params)
        link = content["tracks"]["items"][0]['uri']
        return link

    def get_user_id(self):
        url_endpoint = "https://api.spotify.com/v1/me"
        headers = self.get_resourse_OAuth_2_header()
        r = requests.get(url_endpoint, headers=headers)
        data = r.json()
        user_id = data["id"]
        return user_id


    def get_user_playlists(self):
        url_endpoint = "https://api.spotify.com/v1/me/playlists"
        headers = self.get_resourse_OAuth_2_header()
        print(headers)
        data = requests.get(url_endpoint, headers=headers)
        return data.json()

    def create_user_playlist(self):

        headers = self.get_resourse_OAuth_2_header()
        user_id = self.user_id
        url_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"

        data = {
          "name": input("Enter the name of Playlist: "),
          "public": False
        }

        content = requests.post(url_endpoint, json=data, headers=headers)
        self.playlist_id = content.json()['id']
        pprint(content.json())


    def add_item_to_playlist(self, songs_list_uri):
        headers = self.get_resourse_OAuth_2_header()
        playlist_id = self.playlist_id
        headers["Content-Type"] = "application/json"
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        tracks = {
            "uris": songs_list_uri
        }
        r = requests.post(url, json=tracks, headers=headers)
        print(r.text)
