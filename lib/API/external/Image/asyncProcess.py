from lib.API.external.Image.callOpenai import call_openai_api_and_save
from lib.API.external.Shared.searchSongs import search_songs
from lib.API.external.Image.createPlaylist import create_playlist
import time
from datetime import datetime
from lib.utilities.dbAdmin import dbAdmin


def async_process(userRef, image_url, timestamp):
    total_start_time = time.time()
    start_time = time.time()
    try:
        call_openai_api_and_save(userRef, image_url, timestamp)
    except Exception as e:
        print(f"Error in call_openai_api_and_save: {e}")
    finally:
        print(f"Call OpenAI completion time: {time.time() - start_time} seconds")

    start_time = time.time()
    try:
        search_songs(userRef, timestamp)
    except Exception as e:
        print(f"Error in search_songs: {e}")
    finally:
        print(f"Search Songs completion time: {time.time() - start_time} seconds")

    start_time = time.time()
    try:
        create_playlist(userRef, timestamp, image_url)
    except Exception as e:
        print(f"Error in create_playlist: {e}")
    finally:
        print(f"Create Playlist completion time: {time.time() - start_time} seconds")



    # Call dbAdmin to log the operation in the database
    try:
        # Format start and end time as datetime strings for database insertion
        end_time = time.time()
        runtime = end_time - total_start_time 
        total_start_time_formatted = datetime.fromtimestamp(total_start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_time_formatted = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        userRef_str = str(userRef)

        dbAdmin(userRef_str, "Image", "Yes", total_start_time_formatted, end_time_formatted, runtime)
        print("updated runtime database with performance data")
        print(f"Total running time: {runtime} seconds")

    except Exception as e: 
        print(f"failed to call dbAdmin.py with error: {e}")
        print(f"Total running time: {runtime} seconds")
    
