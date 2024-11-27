import firebase_admin
from firebase_admin import credentials, storage
from google.cloud import storage as gcs
import os
import datetime
from lib.auth.auth import GOOGLE_APPLICATION_CREDENTIALS

def upload_image_to_firebase(image, userRef, timestamp):
    try:
        print("Initializing Firebase Admin SDK...")
        cred = credentials.Certificate('/home/snaplist-server/data/credentials/firebaseCredentials.json')
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {'storageBucket': 'store-e9omk8.appspot.com'})
        print("Firebase Admin SDK initialized.")
        
        print("Referencing the storage bucket...")
        bucket = storage.bucket()
        print("Storage bucket referenced.")
        
        print("Defining local image path and destination path in the bucket...")
        destination_blob_name = f'users/{userRef}/image_{timestamp}.jpg'
        
        print("Creating a blob and uploading the image...")
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(image)
        print("Image uploaded.")
        
        print("Making the blob publicly accessible and retrieving its URL...")
        blob.make_public()
        
        print("Generating a signed URL for temporary access using Google Cloud Storage client library...")
        gcs_client = gcs.Client()
        bucket_gcs = gcs_client.bucket(bucket.name)
        blob_gcs = bucket_gcs.blob(blob.name)
        url_with_access_token = blob.public_url
        print(f"File URL with access token: {url_with_access_token}")
        
        return url_with_access_token
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Execution of upload_image_to_firebase completed.")
