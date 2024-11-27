from flask import jsonify
import os
import json
import time

PLACES_FOLDER = './data'

def get_places():
    places_path = os.path.join(PLACES_FOLDER, 'places.json')
    print(f"Polling for places: {places_path}")
    
    for _ in range(60):  # Timeout after 60 seconds
        try:
            if os.path.exists(places_path):
                with open(places_path, 'r') as f:
                    places = json.load(f)
                    return jsonify(places), 200
        except Exception as error:
            print(f"An error occurred while getting places: {error}")
            return jsonify({"error": str(error)}), 500
        time.sleep(1)
    return jsonify({"error": "places.json not found"}), 404
