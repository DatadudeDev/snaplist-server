import re
import json

def extract_json(content):
    # Pattern to match content between triple backticks
    pattern = r'```json\n(.*?)\n```'
    
    # Search for the pattern in the content
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Extract the matched group
        json_string = match.group(1)
        # Convert the JSON string to a Python dictionary
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return None
    else:
        print("No JSON content found")
        return None