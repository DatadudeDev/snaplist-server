def validate_and_correct_playlist_structure(playlist_json):
    if 'playlist' not in playlist_json:
        print("Invalid data: Expected root index 'playlist'")
        return None

    correct_structure = {
        "title": "",
        "artist": ""
    }

    for i, item in enumerate(playlist_json['playlist']):
        # Check if item has all keys from the correct structure
        for key in correct_structure:
            if key not in item:
                print(f"Key '{key}' not found in item {item}, adding key with empty value.")
                item[key] = correct_structure[key]
        
        # Check if there are any keys in item that are not in the correct structure, and replace them
        item_keys = list(item.keys())
        for key in item_keys:
            if key not in correct_structure:
                print(f"Key '{key}' not an expected key in item {item}, replacing with 'title'.")
                # Change the key to 'title', assuming most rogue keys should be 'title'
                item['title'] = item[key]
                del item[key]

        # Update the item in the playlist
        playlist_json['playlist'][i] = item
        
    return playlist_json

