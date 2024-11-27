from flask import Flask
from lib.auth.auth import check_and_refresh_token
from lib.API.internal.getMoods import get_moods
from lib.API.internal.getPlaces import get_places
from lib.API.internal.postMood import post_mood
from lib.API.internal.postInput import post_input
from lib.API.internal.postVoice import post_voice
from lib.API.internal.postImage import post_image
from lib.API.internal.getPlaylist import get_playlist
from lib.API.internal.getPlaylistInput import get_playlist_input
from lib.utilities.streamLog import setup_logging
from lib.utilities.dbAdmin import dbAdmin  # Import dbAdmin
from datetime import datetime
import os
import subprocess
import logging
import atexit
# Initialize logging
setup_logging()

# Initialize Flask app
app = Flask(__name__)

# Attach route functions to the app
app.route('/v1/get_moods', methods=['GET'])(get_moods)
app.route('/v1/get_places', methods=['GET'])(get_places)
app.route('/v1/post_mood', methods=['POST'])(post_mood)
app.route('/v1/post_input', methods=['POST'])(post_input)
app.route('/v1/post_voice', methods=['POST'])(post_voice)
app.route('/v1/post_image', methods=['POST'])(post_image)
app.route('/v1/get_playlist', methods=['GET'])(get_playlist)
app.route('/v1/get_playlist_input', methods=['GET'])(get_playlist_input)



def inhibit_sleep():
    """Prevent the system from sleeping."""
    cmd = ["sudo", "systemd-inhibit", "--what=idle:sleep", "--who=MyApp", "--why='Preventing sleep while server runs'", "--mode=block", "sleep", "infinity"]
    try:
        # Start the subprocess without waiting for it to complete
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        atexit.register(release_inhibit, proc)
        return proc
    except Exception as e:
        logging.error("Failed to start systemd-inhibit: %s", str(e))
        return None

def release_inhibit(proc):
    """Release the sleep inhibition."""
    if proc:
        try:
            proc.terminate()  # Send SIGTERM to the subprocess
            proc.wait()       # Wait for the subprocess to exit
            logging.info("Inhibition released successfully.")
        except Exception as e:
            logging.error("Error releasing inhibition: %s", str(e))



if __name__ == "__main__":
    if not os.path.exists('./data/Metrics/performance.db'):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_time = current_time
        end_time = current_time
        runtime = 0.0
        dbAdmin("init", "Server Start", "N/A", start_time, end_time, runtime)

    check_and_refresh_token()
    app.run(host='0.0.0.0', port=9872)