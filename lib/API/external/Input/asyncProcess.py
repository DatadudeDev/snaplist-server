import time
from datetime import datetime
from lib.utilities.dbAdmin import dbAdmin
from lib.API.external.Shared.callOpenaiInput import call_openai_api_and_save
from lib.API.external.Shared.searchSongs import search_songs
from lib.API.external.Shared.createPlaylistInput import create_playlist
from lib.API.external.Shared.generateImage import generate_image

def async_process(userRef, userInput, timestamp):
    total_start_time = time.time()
    start_time = time.time()
    try:
        generate_image(userRef, userInput, timestamp)
    except Exception as e: 
        print(f"Failed to generate the image: {e}")
    finally:
        print(f"generateImage completion time: {time.time() - start_time} seconds")
        
    start_time = time.time()
    try:
        call_openai_api_and_save(userRef, userInput, timestamp)
    except Exception as e:
        print(f"Failed to call OpenAI API and save input: {e}")
    finally:
        print(f"callOpenai_api_and_save_input completion time: {time.time() - start_time} seconds")

    start_time = time.time()
    try:
        search_songs(userRef, timestamp)
    except Exception as e:
        print(f"Failed to search songs by input: {e}")
    finally:
        print(f"search_songs_input completion time: {time.time() - start_time} seconds")

    start_time = time.time()
    try:
        create_playlist(userRef, timestamp, userInput)
    except Exception as e:
        print(f"Failed to create playlist by input: {e}")
    finally:
        print(f"create_playlist_input completion time: {time.time() - start_time} seconds")
        
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
