import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor
from lib.utilities.normalizeStrings import normalize_string
from lib.utilities.updateLocalSongs import update_local_songs_with_spotify_urls
from lib.auth.auth import API_BASE_URL, refresh_access_token, load_tokens

def search_song(song, headers):
    try:
        query = normalize_string(f"{song['title']} {song['artist']}")
        response = requests.get(API_BASE_URL + 'search', headers=headers, params={'q': query, 'type': 'track', 'limit': 1})
        if response.status_code == 200 and response.json().get('tracks', {}).get('items'):
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"An error occurred while searching for the song: {e}")
        return None

def search_songs(userRef, timestamp):
    try:
        tokens = load_tokens()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')

        headers = {
            'Authorization': f"Bearer {access_token}"
        }
    except Exception as e:
        print(f"An error occurred while loading credentials: {e}")
        return

    file_path = f'./data/tmp/playlist_{userRef}_{timestamp}.json'

    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        with open(file_path, 'r') as f:
            local_songs = json.load(f)
    except Exception as e:
        print(f"An error occurred while opening or reading the file: {e}")
        return

    search_results = []
    with ThreadPoolExecutor(max_workers=25) as executor:
        # Prepare a list of futures
        future_to_song = {executor.submit(search_song, song, headers): song for song in local_songs['playlist'][1:]}
        for future in future_to_song:
            song = future_to_song[future]
            try:
                result = future.result()
                if result:
                    search_results.append(result)
            except Exception as e:
                print(f"An error occurred during song search execution: {e}")

    if not search_results:
        print("No search results found.")
        return

    try:
        updated_local_songs = update_local_songs_with_spotify_urls(search_results, local_songs)
        with open(file_path, 'w') as f:
            json.dump(updated_local_songs, f, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to file: {e}")

