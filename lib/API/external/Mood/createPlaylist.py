import json
import requests
from lib.API.external.Shared.populatePlaylist import populate_playlist
from lib.auth.auth import API_BASE_URL

def create_playlist(userRef, timestamp, mood):
    # Load the access token from the credentials file
    try:
        with open('./data/credentials/spotifyCredentials.json', 'r') as f:
            creds = json.load(f)
            access_token = creds.get('access_token')
    except Exception as e:
        print(f"An error occurred while trying to load credentials: {e}")
        return
    
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    playlist_path = f'./data/tmp/playlist_{userRef}_{timestamp}.json'

    # read the file at the path and load as json
    try:
        with open(playlist_path, 'r') as f:
            playlist = json.load(f)
    except Exception as e:
        print(f"An error occurred while trying to load playlist details: {e}")
        return

    # then access the values
    playlist_name = playlist["playlist"][0]["title"]
    playlist_description = playlist["playlist"][0]["artist"]
    playlist_public = False

    playlist_data = {
        "name": playlist_name,
        "description": playlist_description,
        "public": playlist_public
    }

    create_playlist_url = f"{API_BASE_URL}users/gabe2091/playlists"
    create_playlist_response = requests.post(create_playlist_url, headers=headers, json=playlist_data)

     #Saving the response data into rawPlaylistAPI.json
    try:
        with open('./rawPlaylistAPI.json', 'w') as file:
            file.write(json.dumps(create_playlist_response.json(), indent=4))
    except Exception as e:
        print(f"An error occurred while trying to save the response from creating the playlist: {e}")
        return


    if create_playlist_response.status_code == 201:
        print(f"Playlist '{playlist_name}' created successfully.")
        playlist_id = create_playlist_response.json().get("id")
        playlist_url = create_playlist_response.json()['external_urls']['spotify']  # Get Spotify URL
        context_uri = create_playlist_response.json()['uri']

        # Define the output URL 
        output_url = f'./data/outputs/playlist_{userRef}_{timestamp}.json'

        try:
            with open('./data/moods.json', 'r') as f:
                moods = json.load(f)
        except Exception as e:
            print(f"An error occurred while trying to load moods details: {e}")
            return

        # Check that mood exists in moods
        mood_image_url = None  # initialize mood_image_url
        for elem in moods['moods']:
            if elem['mood'].lower() == mood.lower():  # comparing in lowercase to avoid case mismatch
                mood_image_url = elem['url']
                break

        if mood_image_url is None:
            mood_image_url = """https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pngkey.com%2Fpng%2Ffull%2F147-1472526_dbutt-discord-emoji-dickbutt-meme.png"""

        # Dictionary with url as key and spotify_url as value
        temp_dict = {
            "userRef": userRef,
            "url": playlist_url,
            "mood": mood,
            "name": playlist_name,
            "context_uri": context_uri,
            "description": playlist_description,
            "id": playlist_id,
            "image_url": mood_image_url  # add the image url linked with the mood

        }

        # Writing to spotifyUrl.json
        try:
            with open(output_url, 'w') as json_file:
                json.dump(temp_dict, json_file)
            print("Spotify URL was saved successfully in the playlist.json")
        except Exception as e:
            print("An error occurred while saving the Spotify URL to playlist.json: ", e)
        populate_playlist(userRef, timestamp, playlist_id, playlist_url)
        return None

    elif create_playlist_response.status_code == 429:
        print(f"Too many requests. Please wait and try again later.")
