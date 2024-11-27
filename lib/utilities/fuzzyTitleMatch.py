from fuzzywuzzy import fuzz
from lib.utilities.normalizeStrings import normalize_string

def fuzzy_title_match(spotify_title, local_title):
    match_ratio = fuzz.partial_ratio(normalize_string(local_title), normalize_string(spotify_title))
    return match_ratio >= 80