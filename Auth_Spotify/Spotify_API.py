import requests
import spotipy
import base64
import datetime
from SpotifyAPI import Spotify
from urllib.parse import urlencode

client_id = "client_id"
client_secret = "client_secret"

client = Spotify(client_id=client_id, client_secret=client_secret)
client.perform_auth()


access_token = client.access_token
headers = {
    "Authorization": f"Bearer {access_token}"
}

endpoint = "https://api.spotify.com/v1/search"
data = urlencode({"q":"Time", "type":"track"})

lookup_url = f"{endpoint}?{data}"

print(lookup_url)
r = requests.get(lookup_url, headers=headers)
print(r.status_code)
