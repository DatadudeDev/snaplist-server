import requests
import json
import os
from lib.utilities.validatePlaylist import validate_and_correct_playlist_structure
from lib.auth.auth import OPENAI_API_KEY

def call_openai_api_and_save(userRef, mood, timestamp):
    mood = mood.lower()

    try:
        # Read the prompt from the file
        prompt_file_path = f'./data/prompts/{mood}.txt'
        if not os.path.exists(prompt_file_path):
            print("Prompt file does not exist")
            return
        
        with open(prompt_file_path, 'r') as file:
            prompt_text = file.read().strip()
    except Exception as e:
        print(f"An error occurred while reading the prompt file: {e}")

    try:
        # Format the request body according to the required structure
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json',
        }
        body = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant that only speaks JSON. Do not write normal text"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                    ]
                }
            ],
            "max_tokens": 500
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=body)
    except Exception as e:
        print(f"An error occurred while making API request: {e}")

    try:
        # Save the raw, unparsed API reply to .raw.json
        raw_output_path = f'./data/tmp/raw_{userRef}_{timestamp}.json'
        os.makedirs(os.path.dirname(raw_output_path), exist_ok=True)
        with open(raw_output_path, 'w', encoding='utf-8') as raw_output_file:
            json.dump(response.json(), raw_output_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"An error occurred while saving API response to .raw.json file: {e}")

    if response.status_code == 200:
        try:
            data = response.json()
            playlist_content = data['choices'][0]['message']['content']
            sanitized_content = playlist_content.replace('```json\n','').replace('\n```','')
            sanitized_content = sanitized_content.replace('\\', '\\\\')
            try:
                playlist_json = json.loads(sanitized_content)
                playlist_json_cleaned = validate_and_correct_playlist_structure(playlist_json)
            except Exception as e:
                print(f"An error occurred while processing and saving playlist data: {e}")


            # Ensure the directory exists where you want to save file:
            if not os.path.exists('./data/tmp'):
                os.makedirs('./data/tmp')

            # Correctly format the file path
            playlist_path = f'./data/tmp/playlist_{userRef}_{timestamp}.json'
            with open(playlist_path, 'w', encoding='utf-8') as playlist_file:
                json.dump(playlist_json_cleaned, playlist_file, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"An error occurred while processing and saving playlist data: {e}")

    else:
        print(f"Failed to call API, status code: {response.status_code}")