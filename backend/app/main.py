import sys
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
import json
sys.path.insert(0, r'../backend/')
from db.consts import *
from scripts import dboperations


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def home():
    return 'O2 sesnsor App is running'

@app.route('/sensor/<sensor_id>', methods=['GET'])
def get_sensor_details(sensor_id):
    try:
        results = dboperations.get_specific_sensor(sensor_id)
    except Exception as e:
        return Response(json.dumps({'error':f'Something went wrong while getting sensor {sensor_id} details: {e}'}),500)
    return Response(json.dumps(results),200)

@app.route('/sensors', methods=['GET'])
def get_all_sensors():
    try:
        results = dboperations.get_data()
    except Exception as e:
        return Response(json.dumps({'error':f'Something went wrong while getting all sensor details: {e}'}),500)
    return Response(json.dumps(results),200)

@app.route('/generate_data', methods=['POST'])
def generate_data():
    args = request.args.to_dict()
    n = args.get("number")
    try:
        dboperations.insert_data(int(n))
    except Exception as e:
        return Response(json.dumps({'error':f'Something went wrong while generating sensor data: {e}'}),500)
    return Response(json.dumps({'message':'data generated successfully'}),200)

@app.route('/sensors/filter', methods=['GET'])
def get_filtered_data():
    try:
        args = request.args.to_dict()
        field = args.get('field', None)
        start = args.get('start', '-1y')
        stop = args.get('stop', '1y')
        data_type_of_sensor = args.get('data_type_of_sensor', None)
        results = dboperations.get_flitered_data(field,start,stop,data_type_of_sensor)
    except Exception as e:
        return Response(json.dumps({'error':f'Something went wrong while getting all sensor details: {e}'}),500)
    return Response(json.dumps(results),200)

@app.route('/sensor/add', methods=['POST'])
def post_sensor_data():
    try:
        data = json.loads(request.data)
        resopnse = dboperations.add_data_point(data)
    except Exception as e:
        return Response(json.dumps({'error':f'Something went wrong while adding sensor data: {e}'}),500)
    return Response(json.dumps({'message':f'sensor {resopnse} data added successfully'}),200)

if __name__ == '__main__':  
   app.run(debug = True)