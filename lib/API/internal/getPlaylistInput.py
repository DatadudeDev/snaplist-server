from flask import jsonify, request
import os
import json
import time
from lib.utilities.removeFiles import remove_files

OUTPUTS_FOLDER = './data/outputs'
TMP_FOLDER = './data/tmp/'

def get_playlist_input():
    # get username and timestamp from the request's arguments
    userRef = request.args.get('userRef')
    timestamp = request.args.get('timestamp')
    
    # create paths for the image and json files
    playlist_filename = f"playlist_{userRef}_{timestamp}.json"
    image_filename = f"{userRef}_{timestamp}_image.jpg"
    raw_filename = f"raw_{userRef}_{timestamp}.json"
    prompt_filename = f'prompt_{userRef}_{timestamp}.json'
    playlist_path = os.path.join(OUTPUTS_FOLDER, playlist_filename)
    image_path = os.path.join(OUTPUTS_FOLDER, image_filename)
    tmp_playlist_path = os.path.join(TMP_FOLDER, playlist_filename)
    tmp_raw_path = os.path.join(TMP_FOLDER, raw_filename)    

    print(f"Polling for playlist: {playlist_path}")
    
    for _ in range(60):  # Timeout after 60 seconds
        if os.path.exists(playlist_path):
            with open(playlist_path, 'r') as f:
                try:
                    playlist = json.load(f)
                    remove_files(playlist_path, tmp_playlist_path, tmp_raw_path, image_path)
                    return jsonify(playlist), 200
                except json.JSONDecodeError:
                    print(f"Error: Could not decode the JSON file {playlist_path}") 



        time.sleep(1)
    return jsonify({"error": f"{playlist_filename} not found"}), 404
