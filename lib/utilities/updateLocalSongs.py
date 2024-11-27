from lib.utilities.fuzzyTitleMatch import fuzzy_title_match
from lib.utilities.normalizeStrings import normalize_string


def update_local_songs_with_spotify_urls(spotify_data, local_data):
    spotify_tracks = {}
    for track_data in spotify_data:
        for item in track_data.get('tracks', {}).get('items', []):
            title = item['name']
            spotify_tracks[title] = item['uri']
    
    # Start loop from index 1
    for song in local_data['playlist'][1:]:
        local_title = normalize_string(song['title'])
        found = False
        for spotify_title, spotify_url in spotify_tracks.items():
            if fuzzy_title_match(spotify_title, local_title):
                song['uri'] = spotify_url  # Changed key to 'spotify_url'
                found = True
                break
        if not found:
            song['uri'] = None  # Assign None if no match found
    
    return local_data
