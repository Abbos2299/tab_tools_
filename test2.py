import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

# Path to your Firebase Admin SDK credentials JSON file
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')

# Initialize Firebase app
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def get_user_info(uid):
    # Access the 'users' collection and retrieve the document with the given UID
    user_doc_ref = db.collection('users').document(uid)
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
                return mc, 'MC'
            elif usdot:
                return usdot, 'USDOT'
            else:
                return None, None
        else:
            return None, None
    else:
        return None, None

def search_company(mc_usdot):
    url = 'https://safer.fmcsa.dot.gov/CompanySnapshot.aspx'
    params = {'SearchType': 'Company',
              'Dbn': mc_usdot}

    response = requests.get(url, params=params)
    time.sleep(3)  # Wait for 3 seconds to allow the page to load

    if 'No records matching' in response.text or 'Record Not Found' in response.text:
        return 'No records'
    else:
        # Parse the response to extract the company phone number
        # You may need to use a HTML parsing library like BeautifulSoup for this step

        # Assuming the extracted phone number is stored in a variable called 'company_phone'
        return company_phone

def update_firestore(uid, mc_usdot, phone):
    user_doc_ref = db.collection('users').document(uid)
    user_doc_ref.update({'Snapshot check': 'No records', 'Company Phone': phone})

# Example usage
user_uid = 'your_user_uid'

mc_usdot, field = get_user_info(user_uid)
if mc_usdot and field:
    company_phone = search_company(mc_usdot)
    if company_phone == 'No records':
        update_firestore(user_uid, mc_usdot, None)
    else:
        update_firestore(user_uid, mc_usdot, company_phone)
