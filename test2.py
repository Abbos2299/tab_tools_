from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import timedelta
import requests
import time
import urllib.parse
import os

app = Flask(__name__)
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)

@app.route('/launch', methods=['GET'])
def launch_python_file():
    user_uid = request.args.get('uid')
    print('User UID:', user_uid)

    # Get Firestore client
    db = firestore.client()

    # Access the 'users' collection and retrieve the document with the given UID
    user_doc_ref = db.collection('users').document(user_uid)
    user_doc = user_doc_ref.get()

    if user_doc.exists:
        # Access the 'User Info' subcollection and retrieve the only document in it
        user_info_collection_ref = user_doc_ref.collection('User Info')
        user_info_docs = user_info_collection_ref.get()

        if len(user_info_docs) == 1:
            user_info_doc = user_info_docs[0]
            mc = user_info_doc.get('MC')
            usdot = user_info_doc.get('USDOT')

            if mc:
                mc_usdot = mc
                search_field = 'MC'
            elif usdot:
                mc_usdot = usdot
                search_field = 'USDOT'
            else:
                mc_usdot = None
                search_field = None

            if mc_usdot and search_field:
                # URL encode the MC/USDOT number
                mc_usdot_encoded = urllib.parse.quote(mc_usdot)

                # Build the URL for the search
                url = f'https://safer.fmcsa.dot.gov/CompanySnapshot.aspx?SearchType=Company&Dbn={mc_usdot_encoded}'

                # Send the request to the website
                response = requests.get(url)
                time.sleep(3)  # Wait for 3 seconds to allow the page to load

                if 'No records matching' in response.text or 'Record Not Found' in response.text:
                    # Update Firestore with 'Snapshot check' field
                    user_doc_ref.update({'Snapshot check': 'No records'})
                else:
                    # Parse the response to extract the company phone number
                    # You may need to use a HTML parsing library like BeautifulSoup for this step
                    # Assuming the extracted phone number is stored in a variable called 'company_phone'
                    company_phone = '1234567890'  # Replace with the actual extracted phone number

                    # Update Firestore with 'Company Phone' field
                    user_doc_ref.update({'Company Phone': company_phone})

                    print(f'Company Phone: {company_phone}')

            else:
                print('MC or USDOT field is missing in User Info')

        else:
            print('User Info document not found')

    else:
        print('User document not found')

    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
