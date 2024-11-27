from flask import jsonify
import os
import json
import time

MOODS_FOLDER = './data'

def get_moods():
    moods_path = os.path.join(MOODS_FOLDER, 'moods.json')
    print(f"Polling for moods: {moods_path}")
    
    for _ in range(60):  # Timeout after 60 seconds
        try:
            if os.path.exists(moods_path):
                with open(moods_path, 'r') as f:
                    moods = json.load(f)
                    return jsonify(moods), 200
        except Exception as error:
            print(f"An error occurred while getting moods: {error}")
            return jsonify({"error": str(error)}), 500
        time.sleep(1)
    return jsonify({"error": "moods.json not found"}), 404
