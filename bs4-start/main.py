import spotipy
import os
import requests
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

SPOTIFY_CLIENT_ID = os.environ.get("client_id")
SPOTIFY_CLIENT_SECRET = os.environ.get("client_secret")
REDIRECT_URI = "https://www.google.com/"

date = input("Which year do you want to travel to ? Type the date in in this format YYYY-MM-DD.")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_web = response.text
soup = BeautifulSoup(billboard_web, "html.parser")
songs_info = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in songs_info]
# print(song_names)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private playlist-modify-public playlist-read-private",
        redirect_uri=REDIRECT_URI,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="d0sy20kbfguudzuvegth3w5mb"
    )
)

users_id = sp.current_user()["id"]

song_uris = []

year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# pprint(song_uris)

new_playlist = sp.user_playlist_create(user=users_id, name=f"{date} billboard 100")

playlist_info = sp.user_playlists(user=users_id)
playlist_id = playlist_info["items"][0]['id']

add_track = sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
