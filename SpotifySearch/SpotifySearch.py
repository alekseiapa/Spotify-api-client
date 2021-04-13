from SpotifyClass import SpotifyAPI
import datetime
import base64
import requests
from urllib.parse import urlencode
from pprint import pprint

Client_ID = "Client_ID"
Secret_Key = "Secret_Key"


spotify = SpotifyAPI(Client_ID, Secret_Key)
spotify.perform_auth()

access_token = spotify.access_token
utl_search_endpoint = "https://api.spotify.com/v1/search"

headers = {
    "Authorization": f"Bearer {access_token}"
}

data = {"q":"Sucker", "type": "track"}
data_encode = urlencode(data)
print(data_encode)
url_to_search = f"{utl_search_endpoint}?{data_encode}"
r = requests.get(url_to_search, headers=headers)
pprint(r.json())
