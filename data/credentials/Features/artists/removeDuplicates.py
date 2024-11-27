import json

# Load the data from the JSON file
with open('./artists.json', 'r') as file:
    data = json.load(file)

# Remove duplicates by converting the list to a set and back to a list
unique_artists = list(set(data['artists']))

# Update the original data with the unique list
data['artists'] = unique_artists

# Write the updated data back to the JSON file
with open('./artists.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Duplicates removed and file updated.")
