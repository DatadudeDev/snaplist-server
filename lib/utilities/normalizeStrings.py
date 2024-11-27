import re

def normalize_string(s):
    return re.sub(r'[^\w\s-]', '', s).lower().strip()