from bs4 import BeautifulSoup
import requests

#2000-08-12
user_answer = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_answer}")
data = response.text
content = BeautifulSoup(data, "html.parser")
chart_element_song = content.find_all(name="span",class_="chart-element__information__song text--truncate color--primary")
chart_element_artist = content.find_all(name="span",class_="chart-element__information__artist text--truncate color--secondary")
songs = [song.string for song in chart_element_song]
artists = [artist.string for artist in chart_element_artist]
songs_dict = []
for i in range(1,101):
    song = {
        i: {
            "song": songs[i-1],
            "artist": artists[i-1]
        }
    }
    songs_dict.append(song)
print(songs)
print(artists)

