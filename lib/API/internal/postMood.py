from flask import request, jsonify
from threading import Thread
from lib.API.external.Mood.asyncProcess import async_process
import time

def post_mood():
    timestamp = int(time.time())
    data = request.json
    userRef = data.get('userRef')
    mood = data.get('mood')
    print(mood)

    
    thread = Thread(target=async_process, args=(userRef, mood, timestamp))
    thread.start()

    # Immediately acknowledge the receipt of the API call
    return jsonify({"timestamp": timestamp}), 202