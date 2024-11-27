from flask import request, jsonify
from threading import Thread
from lib.API.external.Input.asyncProcess import async_process
import time

def post_input():
    timestamp = int(time.time())
    data = request.json
    userRef = data.get('userRef')
    userInput = data.get('input')
    print(userInput)


    thread = Thread(target=async_process, args=(userRef, userInput, timestamp))
    thread.start()

    # Immediately acknowledge the receipt of the API call
    return jsonify({"timestamp": timestamp}), 202
