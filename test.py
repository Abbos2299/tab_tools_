from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from datetime import timedelta
import time
import requests

app = Flask(__name__)
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)

def ocr_space_file(file_url):
    payload = {
        'apikey': 'K89929856188957',
        'url': file_url,
        'language': 'eng',
        'isOverlayRequired': True,
        'detectOrientation': True,
        'isTable': False,
        'scale': False,
        'isCreateSearchablePdf': False,
        'OCREngine': 2,
    }

    response = requests.get('https://api.ocr.space/parse/imageurl', params=payload)
    result = response.json()

    if 'ParsedResults' in result:
        for parsed_result in result['ParsedResults']:
            print(parsed_result['ParsedText'])
    else:
        print("Error occurred: ", result['ErrorMessage'])

@app.route('/launch', methods=['GET'])
def launch_python_file():
    user_uid = request.args.get('uid')
    print('User UID:', user_uid)

    bucket_name = 'tab-tools.appspot.com'
    bucket = storage.bucket(bucket_name)
    folder_name = user_uid  # Replace with the appropriate user UID
    blobs = bucket.list_blobs(prefix=folder_name)

    # Wait for 5 seconds
    time.sleep(5)

    # Iterate over the blobs and get the last added file
    last_added_blob = None
    for blob in blobs:
        if not last_added_blob or blob.updated > last_added_blob.updated:
            last_added_blob = blob

    if last_added_blob:
        file_url = last_added_blob.generate_signed_url(expiration=timedelta(minutes=15))
        print('Last added file URL:', file_url)
        ocr_space_file(file_url)
    else:
        print('No files found in the folder')

    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
