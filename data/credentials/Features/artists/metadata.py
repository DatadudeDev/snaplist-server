import requests
import json
import os

# Assuming this is your OpenAI API key
OPENAI_API_KEY = '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'

def fetch_metadata(artist_name):
    prompt = f"""You only speak JSON. Provide metadata for the artist {artist_name}. "era" is the decade of highest celebrity, "trivia" is a trivlea factoid about the artist, and "genre" is the musical genre of {artist_name}. Map your responses in the JSOn to the indices "era", "trivia", and "genre". """
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    body = {
        "model": "gpt-4-turbo-preview",
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that only speaks JSON. Do not write normal text"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=body)
    
    if response.status_code == 200:
        try:
            data = response.json()
            # Assuming the API's response structure is correctly understood, the following line might need adjustments
            return json.loads(data['choices'][0]['message']['content'])
        except json.JSONDecodeError:
            print("Failed to decode JSON from OpenAI response.")
            return None
    else:
        print(f"Failed to fetch metadata, status code: {response.status_code}")
        return None

def fetch_and_save_artist_metadata(artist_data_file_path, updated_artist_data_file_path):
    try:
        # Load the data from the JSON file
        if not os.path.exists(artist_data_file_path):
            print("Artist data file does not exist.")
            return

        with open(artist_data_file_path, 'r') as file:
            artists_data = json.load(file)

        updated_artists_data = []

        for artist_name in artists_data:
            metadata = fetch_metadata(artist_name)
            print(metadata)
            if metadata:  # Only add if metadata was successfully fetched
                updated_artists_data.append({
                    "name": artist_name,
                    "era": metadata.get('era', 'Unknown'),
                    "trivia": metadata.get('trivia', 'None'),
                    "genre": metadata.get('genre', 'Various')
                })

        # Ensure the directory exists where you want to save the updated data file
        os.makedirs(os.path.dirname(updated_artist_data_file_path), exist_ok=True)

        # Update the original file with the new data
        with open(updated_artist_data_file_path, 'w') as file:
            json.dump(updated_artists_data, file, indent=4)

        print("Metadata updated and file saved.")

    except Exception as e:
        print(f"An error occurred during the process: {e}")

# Example usage
artist_data_file_path = './artists.json'
updated_artist_data_file_path = './updated_artists.json'
fetch_and_save_artist_metadata(artist_data_file_path, updated_artist_data_file_path)