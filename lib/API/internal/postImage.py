from flask import request, jsonify
from threading import Thread
from lib.API.external.Image.asyncProcess import async_process
import time

def post_image():
    timestamp = int(time.time())
    data = request.json
    userRef = data.get('userRef')
    image_url = data.get('imageUrl')
    print(userRef)
    print(image_url)
    
    thread = Thread(target=async_process, args=(userRef, image_url, timestamp))
    thread.start()

    # Immediately acknowledge the receipt of the API call
    return jsonify({"timestamp": timestamp}), 202
