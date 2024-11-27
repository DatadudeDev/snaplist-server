import json
import requests
from lib.API.external.Shared.populatePlaylist import populate_playlist
from lib.API.external.Shared.firebase import upload_image_to_firebase
from lib.auth.auth import API_BASE_URL
from lib.utilities.imageBase64 import image_to_base64


def create_playlist(userRef, timestamp, userInput):

    # Load the access token from the credentials file
    try:
        with open('./data/credentials/spotifyCredentials.json', 'r') as f:
            creds = json.load(f)
            access_token = creds.get('access_token')
            print('loaded access token')

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
            print('loaded playlist')
    except Exception as e:
        print(f"An error occurred while trying to load playlist details: {e}")
        return

    # then access the values
    playlist_name = playlist["playlist"][0]["name"]
    playlist_description = playlist["playlist"][0]["description"]
    playlist_public = False

    playlist_data = {
        "name": playlist_name,
        "description": playlist_description,
        "public": playlist_public
    }

    create_playlist_url = f"{API_BASE_URL}users/gabe2091/playlists"
    create_playlist_response = requests.post(create_playlist_url, headers=headers, json=playlist_data)

    # Saving the response data into rawPlaylistAPI.json
    #try:
    #    with open('./rawPlaylistAPI.json', 'w') as file:
    #        file.write(json.dumps(create_playlist_response.json(), indent=4))
    #except Exception as e:
    #    print(f"An error occurred while trying to save the response from creating the playlist: {e}")
    #    return


    if create_playlist_response.status_code == 201:
        print(f"Playlist '{playlist_name}' created successfully.")
        playlist_id = create_playlist_response.json().get("id")
        playlist_url = create_playlist_response.json()['external_urls']['spotify']  # Get Spotify URL

        # Define the output URL 
        output_url = f'./data/outputs/playlist_{userRef}_{timestamp}.json'
        upload = f'./data/outputs/{userRef}_{timestamp}_image.jpg'
        upload_image_url = upload_image_to_firebase(upload, userRef, timestamp)
        context_uri = create_playlist_response.json()['uri']


        # Dictionary with url as key and spotify_url as value
        temp_dict = {
            "userRef": userRef,
            "url": playlist_url,
            "name": playlist_name,
            "description": playlist_description,
            "id": playlist_id,
            "context_uri": context_uri,
            "image_url": upload_image_url,  # add the image url linked with the input
        }

        # Writing to spotifyUrl.json
        try:
            with open(output_url, 'w') as json_file:
                json.dump(temp_dict, json_file)
            print("Spotify URL was saved successfully in the playlist.json")
        except Exception as e:
            print("An error occurred while saving the Spotify URL to playlist.json: ", e)
        try:
            populate_playlist(userRef, timestamp, playlist_id, playlist_url)
            print("successfully populated playlist")
        except:
            print("failed to populate the playlist")

    elif create_playlist_response.status_code == 429:
        print(f"Too many requests. Please wait and try again later.")
