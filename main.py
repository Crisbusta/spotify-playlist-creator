import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from pprint import pprint
import os

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = "http://example.com"

date = input("A que año te gustaría viajar? Escribe el año en este formato AAAA-MM-DD\n")
BILLBOARD_WEB = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=BILLBOARD_WEB)
billboard = response.text

soup = BeautifulSoup(billboard, "html.parser")
# print(soup.find_all(name="div", class_="o-chart-results-list-row-container"))
top_songs = soup.find_all(name="div", class_="o-chart-results-list-row-container")
songs = [song.find(name="h3", id="title-of-a-story").getText().strip() for song in top_songs]
print(songs)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]

for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. #Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
