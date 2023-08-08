from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from datetime import timedelta
import time
import requests
import urllib.parse
import os
import re
from collections import Counter


app = Flask(__name__)
cred = credentials.Certificate('tab-tools-firebase-adminsdk-8ncav-4f5ccee9af.json')
firebase_admin.initialize_app(cred)

def ocr_space_file(file_path, language, detect_orientation, is_create_searchable_pdf, scale, is_table, ocr_engine):
    payload = {
        'apikey': 'K89929856188957',
        'language': language,
        'detectOrientation': detect_orientation,
        'isCreateSearchablePdf': is_create_searchable_pdf,
        'scale': scale,
        'isTable': is_table,
        'OCREngine': ocr_engine,
    }

    with open(file_path, 'rb') as f:
        result = requests.post('https://api.ocr.space/parse/image', 
                               files={'filename': f},
                               data=payload).json()

    if 'ParsedResults' in result:
        ocr_text = ' '.join([parsed_result['ParsedText'] for parsed_result in result['ParsedResults']])
        broker_names = [
            'AFC Brokerage', 'AFC Logistics', 'Agricultural Logistics, LLC', 'AIT Truckload Solutions', 'Allen Lund',
            'Alliance Highway Capacity', 'ALLY LOGISTICS LLC', 'AM Transport Services, Inc', 'American Group, LLC',
            'American Sugar Refining, Inc.', 'American Transportation Group, LLC', 'Amsino', 'ArcBest Dedicated, LLC',
            'Archerhub', 'Armstrong Transport Group', 'Arrive Logistics', 'ASCEND, LLC', 'ATS Logistics Services, Inc',
            'Axle Logistics', 'B. R. Williams Trucking, Inc', 'BAT Logistics', 'Best Logistics', 'BFT Trucking',
            'BMM Logistics', 'BZS TRANSPORT', 'C.H. Robinson', 'C&L Logistics, Inc', 'Capable Transport, Inc.',
            'CAPITAL LOGISTICS GROUP', 'Cardinal Logistics Management Corp.', 'CarrierHawk', 'Centerstone Logistics',
            'Chariot Logistics', 'Circle Logistics, Inc', 'Commodity Transportation Services, LLC',
            'Concept International Transportation', 'Confiance LLC', 'COYOTE', 'Creech Brokerage, Inc',
            'CRST The Transportation Solution, Inc', 'Custom Pro Logistics llc', 'CW Carriers USA Inc',
            'Czechmate Logistics Inc.', 'D2 FREIGHT SOLUTIONS, LLC', 'DestiNATION Transport, LLC', 'DIAMOND LOGISTICS',
            'Direct Connect Transport, Inc.', 'DYNAMIC LOGISTIX', 'Dynamo Freight LLC', 'EASE Logistics Services',
            'Echo Global Logistics', 'Edge Logistics', 'ELI Solutions, LLC', 'ELIT Transit Solutions, LLC',
            'EMERGE TECH LLC', 'England Logistics', 'eShipping, LLC', 'Evans Delivery Company, Inc',
            'EVE INTERNATIONAL LOGISTICS INC', 'everest transportation system', 'EXPRESS LOGISTICS, INC', 'Fastmore',
            'FEDEX CUSTOM CRITICAL FREIGHT SOLUTIONS', 'FIFTH WHEEL FREIGHT, LLC', 'FreedomTrans USA, LLC',
            'Freezpak Logistics', 'FreightEx Logistics, LLC', 'Frontier Logistics LLC', 'GIX Logistics, Inc',
            'GlobalTranz', 'GO2 EXPRESS', 'Gulf Relay Logistics, LLC', 'Haines City Truck Brokers', 'Hazen Transfer',
            'High Tide Logistics', 'InstiCo', 'ITF LOGISTICS GROUP LLC', 'ITS LOGISTICS LLC', 'J.B. Hunt Transport, Inc',
            'JEAR Logistics, LLC', 'John J. Jerue Truck Broker, Inc.', 'K & L FREIGHT MANAGEMENT',
            'Keller Freight Solutions', 'Kenco Transportation Management LLC', 'KLG Logistics Services, LLC',
            'Kodiak Transportation, LLC', 'Koola Logistics', 'Landmark Logistics, Inc', 'LandStar Global Logistics',
            'LANDSTAR INWAY', 'Landstar Ranger', 'LIBERTY COMMERICAL', 'LinQ Transport, Inc', 'Loadsmart',
            'Logistic Dynamics LLC', 'Logistics One Brokerage, Inc.', 'Longship', 'Magellan Transport Logistics',
            'Marathon Transport, Inc', 'Marten Transport Logistics LLC', 'Max Trans Logistics of Chattanooga LLC',
            'McLeod Logistics', 'MDB Logistics', 'Meadow Lark Agency, Inc', 'megacorp logistics',
            'MIDWEST EXPRESS FREIGHT SOLUTIONS', 'Moeller Logistics', 'MoLo Solutions', 'Motus Freight',
            'Navajo Expedited', 'Network Transport', 'NFI Brokerage', 'Nolan Transportation Group, LLC',
            'NORTHEAST LOGISTICS', 'Old Frontier Family Inc', 'OpenRoad Transportation, Inc.',
            'Packer Transportation & Logistics', 'PAM Transport Inc', 'PATHMARK TRANSPORTATION',
            'Patterson Companies', 'Paul Logistics, Inc', 'Payne Trucking Co.', 'PEPSI LOGISTICS COMPANY, INC.',
            'Performance Logistics', 'Perimeter Logistics LLC', 'PHOENIX SUPPLY CHAIN', 'PINK PANTHERS',
            'PLS Logistics Services', 'Priority 1 Inc', 'R & R Freight Logistics, LLC', 'RB Humphreys',
            'Red Classic', 'Redwood logistics', 'REED TRANSPORT', 'Reliable Transportation Solutions', 'RFX',
            'RJ Logistics, LLC', 'RJS', 'ROAR LOGISTICS', 'ROYAL TRANSPORTATION SERVICES', 'RPM carrier', 'RXO, Inc.',
            'RYAN TRANSPORTATION SERVICE, INC', 'S & H Transport, Inc.', 'S and S Nationwide',
            'Scan Global Logistics', 'Schneider Shipment', 'Scotlynn USA Division', 'Simple Logistics, LLC',
            'Spartan Logistics Services, LLC', 'SPI Logistics', 'Spirit Logistics', 'Spot Freight',
            'Starland Global Logistics LLC', 'Summit Eleven Inc.', 'Sunrise Logistics, Inc.',
            'Surge Transportation Inc', 'Synchrogistics LLC', 'TAYLOR LOGISTICS, INC', 'TERRY ENTERPRISES, INC.',
            'The Worthington Company', 'Thomas E. Keller Trucking, INC.', 'TII Logistics Inc', 'TORCH LOGISTICS, LLC',
            'Torch3pl', 'Total Quality Logistics', 'TRAFFIX', 'Trailer Bridge', 'TransAm Logistics, Inc',
            'Transfix', 'TRANSLOOP', 'Trident Transport, LLC', 'Trinity Logistics, Inc', 'TRIPLE T TRANSPORT, INC',
            'UNIVERSAL CAPACITY SOLUTIONS', 'Unlimited Logistics', 'US1 Network', 'USAT Logistics',
            'Value Logistics Inc', 'VERIHA LOGISTICS', 'Veritiv Logistics Solutions', 'West Motor Freight of PA',
            'WORLDWIDE EXPRESS GLOBALTRANZ', 'XPO Logistics, LLC', 'Yellow Logistics', 'Zengistics Solutions Inc'
        ]
        
    # if 'ParsedResults' in result:
    #     for parsed_result in result['ParsedResults']:
    #         print(parsed_result['ParsedText'])
    
    broker_names_regex = '|'.join([re.escape(broker) for broker in broker_names])
    found_broker_names = re.findall(broker_names_regex, ocr_text, re.IGNORECASE)

        if found_broker_names:
            most_common_broker = Counter(found_broker_names).most_common(1)[0][0]
            print('Most used broker name:', most_common_broker)
        else:
            print('No broker names found in the OCR text')
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
        file_name = urllib.parse.unquote(last_added_blob.name.split('/')[-1])  # Get the file name from the blob URL
        file_url = last_added_blob.generate_signed_url(expiration=timedelta(minutes=15))
        print('Last added file URL:', file_url)
        # Download the file from Firebase
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

        print(f'File "{file_name}" downloaded successfully')
        
        # Perform OCR on the downloaded file
        ocr_space_file(file_name, 'eng', True, False, False, False, '2')

     # Wait for 20 seconds
        time.sleep(20)

        # Delete the file
        os.remove(file_name)
        print(f'File "{file_name}" deleted successfully')
    else:
        print('No files found in the folder')

    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
