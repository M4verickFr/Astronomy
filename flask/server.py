#!/usr/bin/env python
import os
import docker

from flask import Flask, render_template, jsonify, request, json
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongo:27017")
db = client.Spativis
sn_collection = db["supernovas"]

################################################
#####               PAGES                  #####
################################################

@app.route('/')
def index():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    
    return render_template('index.html')

@app.route('/viewer')
def viewer():
    return render_template('viewer.html')

@app.route('/supernovas')
def supernovas():
    return render_template('supernovas.html')

################################################
#####               ERROR                  #####
################################################

@app.errorhandler(404)
def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404

################################################
#####                API                   #####
################################################
@app.route('/api/extract_sn', methods=['GET'])
def extract_new_supernova():  
    # Check if the extract script is running
    process = os.popen('ps -ef | grep extract.py | grep -v grep').read()
    
    if process:
        pid = process.split()[0]
        return jsonify({'error': 'process already running', 'pid': pid})
                            
    # Run the extract script
    output = os.system('python3 ./scripts/extract.py &')
    
    return jsonify({'status': 'process started', 'output': output})
    


################################################
#####              API SN                  #####
################################################

@app.route('/api/sn', methods=['GET'])
def list_supernovas(): # TODO
    sn = sn_collection.find({},{"_id":0})

    if not sn:
        return jsonify({'error': 'data not found'})
    
    t_sn = list(sn)

    return jsonify(t_sn)

@app.route('/api/sn', methods=['PUT'])
def create_record(): # TODO
    record = json.loads(request.data)
    sn = sn_collection.find_one(record)
    if sn:
        return jsonify({'error': 'data already exists'})
    
    sn = sn_collection.insert_one(record)
    return jsonify({'_id': str(sn.inserted_id)})

@app.route('/api/sn', methods=['POST'])
def update_record(): # TODO
    record = json.loads(request.data)
    sn = sn_collection.find_one(record)
    if not sn:
        return jsonify({'error': 'data not found'})
    
    sn.update(record)
    return jsonify({'_id': str(sn.inserted_id)})

@app.route('/api/sn', methods=['DELETE'])
def delete_record(): # TODO
    record = json.loads(request.data)
    supernova = Supernova.objects(name=record['name']).first()
    if not supernova:
        return jsonify({'error': 'data not found'})
    else:
        supernova.delete()
    return jsonify(supernova.to_json())

@app.route('/api/sn/<id>', methods=['GET'])
def query_record(id): # TODO
    supernova = Supernova.objects(name=id).first()
    if not supernova:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(supernova.to_json())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

