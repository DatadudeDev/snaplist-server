import requests
import json
import os
import re
from lib.utilities.extractJSON import extract_json
from lib.auth.auth import OPENAI_API_KEY
from lib.utilities.validatePlaylist import validate_and_correct_playlist_structure

def call_openai_api_and_save(userRef, userInput, timestamp):
    try:
        # Read the prompt from the file
        prompt_file_path = './data/prompts/custom.txt'
        if not os.path.exists(prompt_file_path):
            print("Prompt file does not exist")
            return
        
        with open(prompt_file_path, 'r') as file:
            prompt_text = file.read().strip()
        
        # Splicing in the "input" variable into the custom.txt
        prompt_text = prompt_text.replace("{input}", userInput)

        # Ensure the directory exists where you want to save file:
        if not os.path.exists('./data/tmp'):
            os.makedirs('./data/tmp')

        # Save the output file to ./data/tmp/prompt_{userRef}_{timestamp}.txt
        prompt_output_path = f'./data/tmp/prompt_{userRef}_{timestamp}.txt'
        with open(prompt_output_path, 'w') as prompt_output_file:
            prompt_output_file.write(prompt_text)
            
    except Exception as e:
        print(f"An error occurred while reading the prompt file and replacing the input variable: {e}")
    
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
                    "content": prompt_text
                }
            ],
            "max_tokens": 500
        }
        for attempt in range(2):
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=body)

            if response.status_code == 200:
                # Save the raw, unparsed API reply to .raw.json
                raw_output_path = './data/tmp/raw.json'
                os.makedirs(os.path.dirname(raw_output_path), exist_ok=True)
                with open(raw_output_path, 'w', encoding='utf-8') as raw_output_file:
                    json.dump(response.json(), raw_output_file, ensure_ascii=False, indent=4)
                data = response.json()
                playlist_content = data['choices'][0]['message']['content']
                sanitized_content = playlist_content.replace('```json\n', '').replace('\n```', '')

                try:
                    sanitized_content = sanitized_content.replace('\\', '\\\\')
                    playlist_json = json.loads(sanitized_content)
                    # Ensure the directory exists where you want to save file:
                    if not os.path.exists('./data/tmp'):
                        os.makedirs('./data/tmp')

                    # Correctly format the file path
                    playlist_path = f'./data/tmp/playlist_{userRef}_{timestamp}.json'
                    with open(playlist_path, 'w', encoding='utf-8') as playlist_file:
                        json.dump(playlist_json, playlist_file, ensure_ascii=False, indent=4)
                    return playlist_path
                except json.JSONDecodeError:
                    # If parsing failed and this was the first attempt, retry API call
                    if attempt == 0:
                        print("Error parsing JSON from API response, retrying...")
                        continue
                    else:
                        print(f"OpenAI output errors after multiple attempted calls")
                        return None
            else:
                print(f"Failed to call API, status code: {response.status_code}")
                return None

    except Exception as e:
        print(f"Error in call_openai_api_and_save function: {e}")
        return None