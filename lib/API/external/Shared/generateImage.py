import requests
import json
import base64

def generate_image(userRef, user_input, timestamp):
    url = 'https://pic.datadude.dev/sdapi/v1/txt2img'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    try:
        # Reading data from the JSON file
        with open('./data/prompts/image.json', 'r') as file:
            data = file.read()
    except Exception as e:
        print("Failed to read the JSON file:", e)
        return None
     # Replacing {userInput} with incoming user input
    data = data.replace('{userInput}', json.dumps(str(user_input))[1:-1])
    print(data[2:150])

    try:
        # Making the POST request to the API
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # This will raise an error for bad status
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
        return None
    except requests.exceptions.RequestException as e:
        print("Error in making the request:", e)
        return None
    except Exception as e:
        print("An unexpected error occurred during the request:", e)
        return None

    try:
        # Extracting the 'images' content from the response
        json_response = response.json()
        images = json_response['images']
        
        # Decoding base64 images and saving them
        for i, img in enumerate(images):
            img_data = base64.b64decode(img)
            filename = f'./data/outputs/{userRef}_{timestamp}_image.jpg'  # Creating unique filenames for each image
            with open(filename, 'wb') as f:
                f.write(img_data)
            print('image saved')

        return img_data
    except Exception as e:
         print("Failed to parse the response JSON:", e)
