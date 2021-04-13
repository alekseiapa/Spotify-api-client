from bs4 import BeautifulSoup
from pprint import pprint
import requests
from RobustQuerySearch import SpotifyAPI
import webbrowser

Client_ID = "Client_ID"
Secret_Key = "Secret_Key"
Redirect_uri = "Redirect_uri"
year_search = input("Please enter the year to search YYY-MM-DD : ") #2019-03-10


response = requests.get(f"https://www.billboard.com/charts/hot-100/{year_search}")
data = response.text
content = BeautifulSoup(data, "html.parser")

spotify = SpotifyAPI(Client_ID, Secret_Key, Redirect_uri)

song_name = content.find_all(class_="chart-element__information__song text--truncate color--primary")
song_artist = content.find_all(class_="chart-element__information__artist text--truncate color--secondary")

song_names = [song.string for song in song_name]
song_artist = [artist.string for artist in song_artist]

songs_artists = []
links = []

for i in range(0,100):
    dict_song = {
        "song": song_names[i],
        "artist": song_artist[i]
    }
    songs_artists.append(dict_song)

for song in songs_artists[:5]:
    try:
        links.append(spotify.get_link(query={"artist": song["artist"], "track": song["song"]}, search_type="track"))
    except IndexError:
        print(f"{song['artist']} - {song['song']} doesn't exist in Spotify. Skipped.")


spotify.create_user_playlist()
spotify.add_item_to_playlist(links)
