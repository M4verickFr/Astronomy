#!/usr/bin/env python

import os
import shutil
from datetime import datetime
from pymongo import MongoClient

source_folder = '/data/images/'
destination_folder = '/data/images_in_progress/'

# Create export folder if not exist
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

# Create export folder if not exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

while  len(os.listdir(source_folder)) > 0:
    file_count = 0
    for filename in os.listdir(source_folder):
        if file_count >= 10:
            break
        source = os.path.join(source_folder, filename)
        destination = os.path.join(destination_folder, filename)
        if os.path.isfile(source):
            shutil.move(source, destination)
            file_count += 1

    # Start activation
    if (os.path.exists('/data/hips/')):
        os.system(f"java -Xmx16g -jar scripts/AladinBeta.jar -hipsgen in={destination_folder} out=/data/hips/UNK.AUTH_P_HiPSID creator_did=HiPSID APPEND partitioning=false mixing=false")
    else:
        os.system(f"java -Xmx16g -jar scripts/AladinBeta.jar -hipsgen -live in={destination_folder} out=/data/hips/ creator_did=HiPSID partitioning=false mixing=false")

    # Define mongo client
    client = MongoClient("mongo:27017")
    db = client.Spativis
    sn_collection = db["supernovas"]

    # Delete activated files and set action in BDD
    for filename in os.listdir(destination_folder):
        sn_collection.update_one({'name': filename[:-5]}, {"$set": { 'activationDate' : datetime.now() }})
        file_path = os.path.join(destination_folder, filename)
        os.remove(file_path)

