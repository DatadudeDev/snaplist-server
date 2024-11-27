import time
from datetime import datetime
from lib.API.external.Shared.callOpenaiInput import call_openai_api_and_save
from lib.API.external.Shared.searchSongs import search_songs
from lib.API.external.Shared.createPlaylistInput import create_playlist
from lib.API.external.Shared.generateImage import generate_image
from lib.API.external.Voice.transcribeAudio import transcribe_audio
from lib.utilities.dbAdmin import dbAdmin

def async_process(userRef, userVoice, timestamp):
    total_start_time = time.time()

    start_time = time.time()
    try:
        print(userVoice)
        # Now passing userRef and timestamp to transcribe_audio as required by its new signature
        transcription = str(transcribe_audio(userVoice, userRef, timestamp))
        print(transcription)

    except Exception as e:
        print(f"Failed to transcribe audio: {e}")
    finally:
        print(f"Transcribed audio completion time: {time.time() - start_time} seconds")

    start_time = time.time()
    try:
        generate_image(userRef, transcription, timestamp)
    except Exception as e:
        print(f"Failed to generate image: {e}")
    finally:
        print(f"Generate Image completion time: {time.time() - start_time} seconds")

    start_time = time.time()
    try:
        call_openai_api_and_save(userRef, transcription, timestamp)
    except Exception as e:
        print(f"Failed to call OpenAI API and save Voice: {e}")
    finally:
        print(f"Call OpenAI API and save Voice completion time: {time.time() - start_time} seconds")

    start_time = time.time()
    try:
        search_songs(userRef, timestamp)
    except Exception as e:
        print(f"Failed to search songs by Voice: {e}")
    finally:
        print(f"Search songs by Voice completion time: {time.time() - start_time} seconds")

    start_time = time.time()
    try:
        create_playlist(userRef, timestamp, transcription)
    except Exception as e:
        print(f"Failed to create playlist by Voice: {e}")
    finally:
        print(f"Create playlist by Voice completion time: {time.time() - start_time} seconds")

    print(f"Total running time: {time.time() - total_start_time} seconds")

    # Call dbAdmin to log the operation in the database
    try:
        # Format start and end time as datetime strings for database insertion
        end_time = time.time()
        runtime = end_time - total_start_time
        total_start_time_formatted = datetime.fromtimestamp(total_start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_time_formatted = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        userRef_str = str(userRef)

        dbAdmin(userRef_str, "Image", "Yes", total_start_time_formatted, end_time_formatted, runtime)
        print("Updated runtime database with performance data")
    except Exception as e:
        print(f"Failed to call dbAdmin with error: {e}")