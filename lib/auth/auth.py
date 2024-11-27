import requests
import json
import os
from datetime import datetime, timedelta
import threading
import time

# Spotify App Credentials
CLIENT_ID = 'SPOTIFY CLIENT ID'
CLIENT_SECRET = 'SPOTIFY CLIENT SECRET'
REDIRECT_URI = 'APP REDIRECT URL'
SCOPE = 'user-read-private user-read-email playlist-modify-private playlist-modify-public playlist-read-private playlist-read-collaborativefrom lib.auth.auth import OPENAI_API_KEY
 user-read-recently-played user-modify-playback-state ugc-image-upload user-read-playback-state user-read-currently-playing app-remote-control streaming user-follow-modify user-follow-read user-read-playback-position user-top-read user-library-modify user-library-read'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
CREDENTIALS_PATH = './data/credentials/spotifyCredentials.json'

#OpenAI Credentials: 
OPENAI_API_KEY = 'OPENAI API KEY'

GOOGLE_APPLICATION_CREDENTIALS='PATH-TO-GOOGLE-SERVICE-ACCOUNT-CREDENTIALS'

def refresh_access_token(refresh_token):
    """Attempt to refresh the Spotify access token using the provided refresh token."""
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get('access_token'), refresh_token
    else:
        print(f"Failed to refresh token, please reauthenticate. Status code: {response.status_code}")
        return None, None

def refresh_token_periodically():
    """Refresh the token every 5 seconds."""
    while True:
        if os.path.exists(CREDENTIALS_PATH):
            with open(CREDENTIALS_PATH, 'r') as file:
                tokens = json.load(file)
            new_access_token, _ = refresh_access_token(tokens['refresh_token'])
            if new_access_token:
                print('Token refreshed successfully.')
                save_or_refresh_tokens(refresh_token=tokens['refresh_token'], access_token=new_access_token)
            else:
                print('Token refresh failed, user needs reauthentication.')
        time.sleep(300)  # Wait for 10 minutes before next refresh

def check_and_refresh_token():
    """Start the refresh token process on a separate thread."""
    thread = threading.Thread(target=refresh_token_periodically, daemon=True)
    thread.start()

def save_or_refresh_tokens(refresh_token=None, access_token=None):
    """Save new tokens or refresh existing ones, and update last_checked timestamp."""
    token_info = {}
    need_to_update_file = False
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH, 'r') as file:
            token_info = json.load(file)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    token_info['last_checked'] = current_time  # Always update last_checked

    if access_token:
        token_info['access_token'] = access_token
        token_info['last_updated'] = current_time  # Update last_updated when the access token is refreshed
        need_to_update_file = True

    if refresh_token:
        token_info['refresh_token'] = refresh_token
        need_to_update_file = True

    if need_to_update_file:
        with open(CREDENTIALS_PATH, 'w') as file:
            json.dump(token_info, file, indent=4)

def load_tokens():
    """Load the access and refresh tokens from a local file, if it exists."""
    try:
        if os.path.exists('./data/credentials/spotifyCredentials.json'):
            print("Loading existing credentials...")
            with open('./data/credentials/spotifyCredentials.json', 'r') as file:
                return json.load(file)
        else:
            print("No credentials found, user needs to authenticate at https://snapli.st")
    except Exception as e:
        print(f"Error loading tokens: {e}")
        return None