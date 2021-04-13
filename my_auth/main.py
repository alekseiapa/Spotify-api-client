import spotipy


SPOTIPY_CLIENT_ID = '3cc99a365444471dac7e9c33fee0936c'
SPOTIPY_CLIENT_SECRET = '9087d509d64d4c2d9731d1bee413f08a'
SPOTIPY_REDIRECT_URI = 'http://example.com/alapas'


auth_object = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI, )

sp = spotipy.client.Spotify(client_credentials_manager=auth_object)
user_name = sp.current_user()['display_name']
user_id = sp.current_user()['id']

print(user_name)
print(user_id)