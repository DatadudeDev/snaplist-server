from flask import request, jsonify
from threading import Thread
from lib.API.external.Voice.asyncProcess import async_process
import time

def post_voice():
    timestamp = int(time.time())
    data = request.json
    userRef = data.get('userRef')
    voice = data.get('voice')

    thread = Thread(target=async_process, args=(userRef, voice, timestamp))
    thread.start()

    # Immediately acknowledge the receipt of the API call
    return jsonify({"timestamp": timestamp}), 202
    
