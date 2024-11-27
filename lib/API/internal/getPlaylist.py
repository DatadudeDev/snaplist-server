from flask import jsonify, request
import os
import json
import time
from lib.utilities.removeFiles import remove_files

OUTPUTS_FOLDER = './data/outputs'
TMP_FOLDER = './data/tmp/'

def get_playlist():
    # get username and timestamp from the request's arguments
    userRef = request.args.get('userRef')
    timestamp = request.args.get('timestamp')
    
    # Polling for the {username}_{timestamp}_playlist.json file
    playlist_filename = f"playlist_{userRef}_{timestamp}.json"
    raw_filename = f"raw_{userRef}_{timestamp}.json"
    image_filename = f"{userRef}_{timestamp}_image.jpg"
    playlist_path = os.path.join(OUTPUTS_FOLDER, playlist_filename)
    tmp_playlist_path = os.path.join(TMP_FOLDER, playlist_filename)
    tmp_raw_path = os.path.join(TMP_FOLDER, raw_filename)
    image_path = os.path.join(OUTPUTS_FOLDER, image_filename)

    # Print the path that is being polled
    print(f"Polling for playlist: {playlist_path}")
    
    for _ in range(60):  # Timeout after 60 seconds
        if os.path.exists(playlist_path):
            with open(playlist_path, 'r') as f:
                playlist = json.load(f)
                                
                remove_files(playlist_path, tmp_playlist_path, tmp_raw_path, image_path)
                return jsonify({**playlist}), 200  # Add context_uri to playlist
        time.sleep(1)
        
    return jsonify({"error": f"{playlist_filename} not found"}), 404
