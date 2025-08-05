import os, json, time
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
PLAYLIST_URL = os.getenv("PLAYLIST_URL")
SLSKD_API = os.getenv("SLSKD_API")
SLSK_USER = os.getenv("SLSK_USER")
SLSK_PASS = os.getenv("SLSK_PASS")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

AUTH = (SLSK_USER, SLSK_PASS)

def get_tracks():
    results = sp.playlist_tracks(PLAYLIST_URL)
    tracks = []
    for item in results['items']:
        track = item['track']
        artist = track['artists'][0]['name']
        title = track['name']
        tracks.append(f"{artist} - {title}")
    return set(tracks)

def search_and_download(query):
    res = requests.post(f"{SLSKD_API}/search", auth=AUTH, json={"query": query})
    results = res.json().get("results", [])
    if results:
        file_id = results[0]["id"]
        dl_res = requests.post(f"{SLSKD_API}/download", auth=AUTH, json={"file_id": file_id})
        print(f"Queued: {query}")
    else:
        print(f"Not found: {query}")

def load_previous():
    try:
        with open("playlist.json") as f:
            return set(json.load(f))
    except:
        return set()

def save(tracks):
    with open("playlist.json", "w") as f:
        json.dump(list(tracks), f)

def main():
    current = get_tracks()
    previous = load_previous()
    new = current - previous
    for track in new:
        search_and_download(track)
        time.sleep(2)
    save(current)

if __name__ == "__main__":
    main()
