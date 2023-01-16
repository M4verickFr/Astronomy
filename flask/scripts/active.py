#!/usr/bin/env python

import os
from datetime import datetime
from pymongo import MongoClient

folder_path = '/data/images/'

# Start activation
if (os.path.exists('/data/hips/')):
    os.system(f"java -Xmx16g -jar scripts/AladinBeta.jar -hipsgen in={folder_path} out=/data/hips/UNK.AUTH_P_HiPSID creator_did=HiPSID APPEND")
else:
    os.system(f"java -Xmx16g -jar scripts/AladinBeta.jar -hipsgen -live in={folder_path} out=/data/hips/ creator_did=HiPSID")

# Define mongo client
client = MongoClient("mongo:27017")
db = client.Spativis
sn_collection = db["supernovas"]

# Delete activated files and set action in BDD
for filename in os.listdir(folder_path):
    sn_collection.update_one({'name': filename[:-5]}, {"$set": { 'activationDate' : datetime.now() }})
    file_path = os.path.join(folder_path, filename)
    os.remove(file_path)

