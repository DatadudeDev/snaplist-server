import requests
import os
import time
import subprocess
from openai import OpenAI
from lib.auth.auth import OPENAI_API_KEY

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=OPENAI_API_KEY)

def download_file(url, userRef, timestamp):
    try:
        local_filename = f"voice_{userRef}_{timestamp}.mp3"
        local_path = f"/home/snaplist-server/data/tmp/{local_filename}"

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"File downloaded successfully: {local_path}")
        return local_path
    except Exception as e:
        print(f"Failed to download the file: {e}")
        return None

def wait_for_file(file_path):
    print("Searching for the file...")
    while not os.path.exists(file_path):
        time.sleep(1)
    print(f"File found: {file_path}")

def inspect_audio_file(file_path):
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 
               'format=format_name', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        result = subprocess.run(cmd, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error inspecting the file: {e}")
        return None

def convert_to_mp3(input_path):
    output_path = input_path.replace(".mp3", "_clean.mp3")
    try:
        cmd = ['ffmpeg', '-i', input_path, '-codec:a', 'libmp3lame', '-q:a', '2', output_path]
        subprocess.run(cmd, check=True)
        print(f"File converted successfully: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert the file: {e}")
        return None

def transcribe_audio(audio_url, userRef, timestamp):
    audio_file_path = download_file(audio_url, userRef, timestamp)
    
    if audio_file_path is None:
        print("The file was not downloaded successfully. Aborting transcription.")
        return None

    wait_for_file(audio_file_path)
    
    # Inspect the audio file to check its format
    audio_format = inspect_audio_file(audio_file_path)
    if audio_format == 'mp3':
        print("Verified file is an MP3. Skipping conversion.")
        clean_audio_file_path = audio_file_path
    else:
        print(f"File format is {audio_format}, converting to MP3.")
        clean_audio_file_path = convert_to_mp3(audio_file_path)
        if clean_audio_file_path is None:
            print("Failed to convert the file to MP3. Aborting transcription.")
            return None

    try:
        with open(clean_audio_file_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )
        transcription_text = transcription.text  # Extract the text from the transcription
        print("Successfully transcribed the audio file:", transcription_text)
    except Exception as e:
        print(f"Failed to transcribe the audio file: {e}")
        return None

    # Remove the files only if a conversion took place
    if clean_audio_file_path != audio_file_path:
        try:
            os.remove(audio_file_path)
        except Exception as e:
            print(f"Failed to remove the original downloaded file: {e}")

    try:
        os.remove(clean_audio_file_path)
        print("Successfully removed the converted file.")
    except Exception as e:
        print(f"Failed to remove the converted file: {e}")
    return transcription_text  # Return the transcription text instead of the whole object

