#part 1
import firebase_admin
from firebase_admin import credentials

#part 2
import requests
import base64
import os
import sys


#part 1
# Initialize Firebase Admin SDK
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)

# Now you're connected to Firebase and can use its services



#part 2
def ocr_space_file(filename, language, overlay, ocr_engine):
    payload = {
        'apikey': 'K89929856188957',
        'language': language,
        'isOverlayRequired': overlay,
        'OCREngine': ocr_engine,
    }

    with open(filename, 'rb') as f:
        result = requests.post('https://api.ocr.space/parse/image', 
                               files={filename: f},
                               data=payload).json()

    if 'ParsedResults' in result:
        for parsed_result in result['ParsedResults']:
            print(parsed_result['ParsedText'])
    else:
        print("Error occurred: ", result['ErrorMessage'])

if __name__ == "__main__":
    filename = '123.pdf'
    language = 'eng'
    overlay = False
    ocr_engine = 2

    ocr_space_file(filename, language, overlay, ocr_engine)



