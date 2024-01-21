import requests
from bs4 import BeautifulSoup
import spotipy
import os
import base64

spotify_endpoint = "https://api.spotify.com/v1"
date = input("Which Year do you want listen to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
data = response.text
soup = BeautifulSoup(data, "html.parser")
titles = soup.select("li ul li h3")
song_names = [thing.getText().strip() for thing in titles]
auth_header = base64.b64encode(f'{os.environ.get("Client ID")}:{os.environ.get("Client secret")}'.encode()).decode()
spotify_headers = {
    'Authorization': f'Bearer {os.environ.get("BEARER")}'
}

spotify_body = {
    "name": f"Top 100 song date: {date}",
    "public": "false",
    "description": "Practice using webscrapping and Spotify API "
}
response_create_playlist = requests.post(url=f"{spotify_endpoint}/users/{os.environ.get("USER_ID")}/playlists",
                                         json=spotify_body,headers=spotify_headers)
playlist_id = response_create_playlist.json()["id"]
uri_list = []
for song in song_names:
    spotify_params = {
        "q": {song},
        "type": "track",
        "limit": 1
    }
    response = requests.get(url=f"{spotify_endpoint}/search", headers=spotify_headers, params=spotify_params)
    data = response.json()["tracks"]["items"][0]["uri"]
    uri_list.append(data)
add_music_body = {
    "uris": uri_list
}
add_music_header = {
    'Authorization': f'Bearer {os.environ.get("BEARER")}',
    "Content-Type": "application/json"
}
add_music = requests.post(url=f"{spotify_endpoint}/playlists/{playlist_id}/tracks", headers=add_music_header,
                          json=add_music_body)
print(add_music.json())






