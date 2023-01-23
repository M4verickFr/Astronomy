#!/usr/bin/env python
import os

from flask import Flask, render_template, jsonify, request, json, send_from_directory, escape
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

@app.route('/data/<path:filename>')
def data(filename):
    return send_from_directory('/data', filename)

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
@app.route('/api/extract_sn/start', methods=['GET'])
def extract_new_supernova():
    # Check if the extract script is running
    process = os.popen('ps -ef | grep extract.py | grep -v grep').read()
    
    if process:
        pid = process.split()[0]
        return jsonify({
            'type': 'error',
            'message': 'Extraction already in progress',
            'pid': pid
        })

    # Run the extract script
    os.system('python3 ./scripts/extract.py &')
    
    return jsonify({
        'type': 'info',
        'message': 'Supernova extraction started'
    })

@app.route('/api/extract_sn/pid', methods=['GET'])
def extract_new_supernova_progress():
    # Check if the extract script is running
    process = os.popen('ps -ef | grep extract.py | grep -v grep').read()
    
    if process:
        pid = process.split()[0]
        return jsonify({
            'type': 'info',
            'message': 'Extraction in progress',
            'pid': pid
        })

    return jsonify({
            'type': 'warning',
            'message': 'No extraction in progress'
        })

@app.route('/api/convert_sn/start', methods=['GET'])
def convert_supernovas():
    image_tag = 'spativis-converter'
    auto_remove = request.args.get('auto_remove') or ""
    auto_remove =  False if auto_remove.lower() == "false" else True
    nb_containers = int(request.args.get('nb_containers') or 10);

    # Check if the image building script is running
    process = os.popen('ps -ef | grep build.py | grep -v grep').read()
    
    if process:
        pid = process.split()[0]
        return jsonify({
            'type': 'info',
            'message': 'Image building in progress',
            'pid': pid
        })

    # Check if build image exist, if not exist, start building it
    if (int(os.popen(f"docker images | grep {image_tag} | wc -l").read()) == 0):
        # Run the image building script
        os.system('python3 ./scripts/build.py &')
        
        return jsonify({
            'type': 'info',
            'message': 'Image not build, start building it',
            'status': 'startImageBuilding'
        })

    os.popen(f"docker rm $(docker container ls -aq -f ancestor={image_tag})")

    # Prevent start too many containers
    if (nb_containers > 20):
        return jsonify({
            'type': 'error',
            'message': 'nb_containers too high'
        })

    # Extract path to data folder
    source_path = os.popen('docker inspect  $(docker container ls -q -f name=astronomy-backend) -f \'{{ range .Mounts }}{{ if eq .Destination "/data" }}{{ .Source }}{{ end }}{{ end }}\'').read().strip()

    # Start x containers
    for x in range(nb_containers):
        os.system(f"docker run --detach --network=astronomy_default -v {source_path}:/data {image_tag}")

    # Extract tags of started containers
    containers = os.popen(f"docker container ls -q -f ancestor={image_tag}").read()

    return jsonify({
        'type': 'success',
        'message': f'{nb_containers} containers started',
        'containers': containers.split("\n")[:-1]
    })

@app.route('/api/convert_sn/pid', methods=['GET'])
def image_is_build():
    # Check if the image building script is running
    process = os.popen('ps -ef | grep build.py | grep -v grep').read()
    
    if process:
        pid = process.split()[0]
        return jsonify({
            'type': 'info',
            'message': 'Image construction in progress',
            'pid': pid
        })

    return jsonify({
            'type': 'warning',
            'message': 'No image construction in progress'
        })

@app.route('/api/active_sn', methods=['GET'])
def active_supernovas():
    # Check if the active script is running
    process = os.popen('ps -ef | grep active.py | grep -v grep').read()
    
    if process:
        pid = process.split()[0]
        return jsonify({
            'type': 'error',
            'message': 'process already running',
            'pid': pid
        })
                            
    # Run the active script
    output = os.system('python3 ./scripts/active.py &')
    
    return jsonify({
        'type': 'info',
        'message': 'process started',
        'output': output
    })

@app.route('/api/reset', methods=['GET'])
def reset():
    output = os.popen('rm -rf /data/*').read()
    sn_collection.delete_many({})
    return jsonify({'status': 'All data reseted', 'output': output})


################################################
#####              API SN                  #####
################################################

@app.route('/api/sn', methods=['GET'])
def list_supernovas():
    filterData = {"activationDate": {"$ne": None}} if request.args.get('active') else {}
    sn = sn_collection.find(filterData,{"_id":0})

    sn_inactive = sn_collection.find({"processingStartDate": None},{"_id":0})
    sn_active = sn_collection.find({"activationDate": {"$ne": None}},{"_id":0})
    sn_processing = sn_collection.find({"processingStartDate": {"$ne": None},"activationDate": None},{"_id":0})

    if not sn or not sn_inactive or not sn_active or not sn_processing:
        return jsonify({'error': 'data not found'})

    sn_inactive = len(list(sn_inactive))
    sn_active = len(list(sn_active))
    sn_processing = len(list(sn_processing))

    total = sn_inactive+sn_active+sn_processing

    return jsonify({
        't_sn': list(sn),
        'sn_inactive': sn_inactive / total,
        'sn_active': sn_active / total,
        'sn_processing': sn_processing / total
    })

@app.route('/api/sn', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    sn = sn_collection.find_one(record)
    if sn:
        return jsonify({'error': 'data already exists'})
    
    sn = sn_collection.insert_one(record)
    return jsonify({'_id': str(sn.inserted_id)})

@app.route('/api/sn', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    sn = sn_collection.find_one(record)
    if not sn:
        return jsonify({'error': 'data not found'})
    
    sn.update(record)
    return jsonify({'_id': str(sn.inserted_id)})

@app.route('/api/sn', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    supernova = Supernova.objects(name=record['name']).first()
    if not supernova:
        return jsonify({'error': 'data not found'})
    else:
        supernova.delete()
    return jsonify(supernova.to_json())

@app.route('/api/sn/<id>', methods=['GET'])
def query_record(id):
    supernova = Supernova.objects(name=id).first()
    if not supernova:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(supernova.to_json())

@app.route('/api/sn_stats', methods=['GET'])
def stats_supernovas():
    sn_inactive = sn_collection.find({"processingStartDate": None},{"_id":0})
    sn_active = sn_collection.find({"activationDate": {"$ne": None}},{"_id":0})
    sn_processing = sn_collection.find({"processingStartDate": {"$ne": None},"activationDate": None},{"_id":0})

    if not sn_inactive or not sn_active or not sn_processing:
        return jsonify({'error': 'data not found'})

    return jsonify({
        'sn_inactive': len(list(sn_inactive)),
        'sn_active': len(list(sn_active)),
        'sn_processing': len(list(sn_processing))
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

