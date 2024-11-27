import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from lib.auth.auth import API_BASE_URL

def save_api_response(data):
    with open('./apiRaw.json', 'w') as file:
        json.dump(data, file)

def add_song_to_playlist(song, headers, playlist_id, playlist_url, attempt=1):
    spotify_uri = song.get('uri')
    song_name = song.get('title')  # Assuming 'title' parameter has the song's name
    playlist_name = playlist_url.split('/')[-1]  # Extracting playlist name from URL

    if spotify_uri is None:
        print("Song has no Spotify URIs. Skipping...")
        return f"Skipped '{song_name}' (no URI)."

    data = {"uris": [spotify_uri], "position": 0}
    url = f"{API_BASE_URL}playlists/{playlist_id}/tracks"

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return f"Added '{song_name}' to the playlist: '{playlist_name}' successfully."
        else:
            if attempt < 2:  # If this is the first attempt, retry once
                print(f"Attempt 1 failed for '{song_name}'. Retrying...")
                return add_song_to_playlist(song, headers, playlist_id, playlist_url, attempt + 1)
            else:  # If this is the second attempt, save API response and move on
                save_api_response(response.json())
                return f"Failed to add '{song_name}' to playlist '{playlist_name}' after 2 attempts. Response code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        if attempt < 2:
            print(f"Attempt 1 failed for '{song_name}'. Retrying...")
            return add_song_to_playlist(song, headers, playlist_id, playlist_url, attempt + 1)
        else:
            save_api_response({"error": str(e)})
            return f"An error occurred while adding '{song_name}' to the playlist '{playlist_name}' after 2 attempts: {e}"

def populate_playlist(userRef, timestamp, playlist_id, playlist_url):
    try:
        with open('./data/credentials/spotifyCredentials.json', 'r') as f:
            creds = json.load(f)
        access_token = creds.get('access_token')
    except Exception as e:
        print(f"Error loading access token: {e}")
        return

    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }

    try:
        with open(f'./data/tmp/playlist_{userRef}_{timestamp}.json', 'r') as f:
            songs = json.load(f)['playlist']
    except Exception as e:
        print(f"Error loading songs from file: {e}")
        return

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(add_song_to_playlist, song, headers, playlist_id, playlist_url) for song in songs[1:]]
        for future in as_completed(futures):
            print(future.result())